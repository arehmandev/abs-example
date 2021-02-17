# Flask Kube api  

## Instructions

```sh
  docker-compose up -d
  # Modify the docker-compose if you want to change image names
  docker-compose build && docker-compose push
  # To shutdown
  docker-compose down



  # List people (feel free to run anytime between below steps)
  curl localhost:5000/people 
  # Adding an item
  curl --header "Content-Type: application/json" --request POST --data @test/data.json localhost:5000/people
  # Modifying the item
  curl --header "Content-Type: application/json" --request PUT --data @test/data2.json localhost:5000/people/1
  # Checking product has been added
  curl localhost:5000/people 
  # Delete product
  curl --header "Content-Type: application/json" --request DELETE localhost:5000/people/1
  # Load people from test CSV
  curl localhost:5000/load 
  # Load your own custom CSV
   curl -F 'file=@test/titanic.csv' localhost:5000/csv
```

## Helm

I've added the helm chart in the helm directory, haven't tested
## Routes  
