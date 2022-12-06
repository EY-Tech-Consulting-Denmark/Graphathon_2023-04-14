# **ATP – EY Hackathon - Answers to Algorithm Questions**

Keep in mind there are multiple solutions to each exercise. Below is just one way to approach the exercises.

## **Centrality**


### **Exercise 2.1 Query through the result using python to determine whether this would be a good feature to add?**
<details>
  <summary> Answer to the execise (Click to expand) </summary>

```
# Query throught the results to see how many claims a physician is involved in and whether that physician is involved with a fraudulent provider
provider_claims = gds.run_cypher(''' 
//Query the database sorting by amount of claims associated with each physician
match (c:Claim)-[]-(pr:Provider)
return distinct pr.id as provider, pr.provider_degree AS claims, pr.fraud as fraud
order by claims desc
''')

print(provider_claims.head())

# Create a plot, plotting the density of the amount of claims associated with a physician for physicians that are associated with a fraudelent provider and non fraudulent providers
graph = provider_claims.groupby('fraud')['claims'].plot(kind='kde', legend = True, xlim=[0,150])
```
See that there is a difference in the distribution. So this would be a good feature.

</details>
<br>

### **Exercise 2.2: Create a new projection that will find the amount of claims are associated with a physician. Determine whether this would be a good feature to add?**

<details>
  <summary> Answer to the execise (Click to expand) </summary>

Start by creating a projection, considering only the claims and the physicians.
```
# Create projection of the claim and physician nodes that includes all the relationships between claim and physician

claim_phys_degree, project_stats  = gds.graph.project(
    'claim_phys',
    ['Claim', 'Physician'],
    ['HAS_ATTENDING', 'HAS_OPERATING', 'HAS_OTHER']
)

project_stats
```

```
# Stream the results to get a quick overview of the results
gds.degree.stream(claim_phys_degree, orientation= 'REVERSE')
```

```
# Write the result back to the original graph by creating a new property on the physician and claim nodes
gds.degree.write(claim_phys_degree, orientation= 'REVERSE', writeProperty='claim_degree')
```

```
# Query throught the results to see how many claims a physician is involved in and whether that physician is involved with a fraudulent provider
degree_query = gds.run_cypher('''
//Query the database sorting by amount of claims associated with each physician
match (p:Physician)-[]-(:Claim)-[]-(pr:Provider)
return distinct p.id as physician, p.claim_degree AS claims , pr.id AS provider , pr.fraud as fraud
order by claims
''')

# Create a plot, plotting the density of the amount of claims associated with a physician for physicians that are associated with a fraudelent provider and non fraudulent providers
print(degree_query.head())
degree_query.groupby('fraud')['claims'].plot(kind='kde', legend = True, xlim=[0,100])
```
See that could be a good feature.

Remember to drop the projection.
```
# Drop the graph projections to save memory or fix mistakes
claim_phys_degree.drop()
```

</details>
<br>

### **Exercise 2.3: Create a new projection that will find the amount of diagnosis that are associated with a claim. Determine whether this would be a good feature to add?**

<details>
  <summary> Answer to the execise (Click to expand) </summary>

Start by creating a projection, considering only the claims and the diagnosis.
```
# Create projection of the claim and physician nodes that includes all the relationships between claim and physician

claim_diag_degree, project_stats  = gds.graph.project(
    'claim_diag',
    ['Claim', 'Diagnosis'],
    ['HAS_DIAGNOSIS_CODE_OF', 'HAS_ADMISSION_WITH', 'HAS_GROUP_CODE_OF']
)

project_stats
```

```
# Stream the results to get a quick overview of the results
gds.degree.stream(claim_diag_degree)
```
NOTE: Here the relationships are not reversed!
```
# Write the result back to the original graph by creating a new property on the physician and claim nodes
gds.degree.write(claim_diag_degree, writeProperty='claim_degree')
```

```
# Query throught the results to see how many diagnosis are asssociated for the claim and whether that claim is involved with a fraudulent provider
claim_diag_degree = gds.run_cypher(''' 
    //Query the database sorting by amount of claims associated with each physician
    match (d:Diagnosis)-[]-(c:Claim)-[]-(pr:Provider)
    return distinct c.id as claim, c.diag_degree AS diagnosis_count , pr.id AS provider , pr.fraud as fraud
    order by diagnosis_count asc
''')
claim_diag_degree.head()

# Create a plot, plotting the density of the amount of diagnosis associated with a claim and if that claim is associated with a fraudelent provider and non fraudulent providers
claim_diag_degree.groupby('fraud')['diagnosis_count'].plot(kind='kde', label = True)
```
See that would not be a good feature.

Remember to drop the projection.
```
# Drop the graph projections to save memory or fix mistakes
claim_phys_degree.drop()
```

</details>
<br>

## **Community Detection**

### **Exercise 3.1: Check the communities that have been found. What is the average claim amount? What providers are above average?**

<details>
  <summary> Answer to the execise (Click to expand) </summary>

```
# Check our communities, what is the average claim amout, and what providers are above average
gds.run_cypher('create range index if not exists for (n:Claim) on (n.community_id)')
community_dist = gds.run_cypher(''' 
    match (n:Claim)
    with n.community_id as community_id, 
            count(*) as number_of_claims,
            avg(n.reimbursedAmt) as avg_community_amt
        order by number_of_claims desc limit 50
    match (c:Claim{community_id:community_id})-[:SUBMITTED_BY]->(p)
    with p, community_id, avg_community_amt, 
            avg(c.reimbursedAmt) as avg_provider_amt
        order by avg_provider_amt desc
        where avg_provider_amt > avg_community_amt
    with p, community_id, avg_community_amt, avg_provider_amt,
        avg_provider_amt/avg_community_amt*100 as percent_over_average
        order by  percent_over_average desc
    return 
        community_id, 
        p.id as provider_id, 
        avg_community_amt, 
        avg_provider_amt,
        percent_over_average,
        p.fraud as is_fraud
    limit 20
''')
community_dist.head(20)
```

</details>

<br>

### **Exercise 3.2: Check the communities that have been found. What is the number of fraudulent providers per community?**

<details>
  <summary> Answer to the execise (Click to expand) </summary>

```
# Check our communities, what are the number of fraudlent providers per community
gds.run_cypher('create range index if not exists for (n:Claim) on (n.community_id)')
community_dist = gds.run_cypher(''' 
    match (n:Claim)-[:SUBMITTED_BY]->(p)
    with 
        n.community_id as community_id, collect(distinct p) as providers
    with
        community_id,
        size([ p in providers where p.fraud = true | 1]) as fradulent_providers, 
        size([ p in providers where p.fraud = false | 1]) as non_fradulent_providers
    with
        community_id, fradulent_providers, non_fradulent_providers,
        100.0*fradulent_providers/(non_fradulent_providers + fradulent_providers) as fraud_percent
    return community_id, fradulent_providers, non_fradulent_providers, fraud_percent order by fraud_percent desc limit 10
''')
community_dist.head(20)
```

</details>
<br>

### **Exercise 3.3: Plot the results.**

<details>
  <summary> Answer to the execise (Click to expand) </summary>

```
# Lets plot it
community_dist.hist('fraud_percent')
```

</details>
