# Architectural Decisions

## Eve Online

I choose Eve as my 3rd party source because of the data fitting my POC concept well. I also have prior experience
working with their API and have built a mapping tool known by the name 'Artemis' for Eve Online.

## Database

Of course choosing Janusgraph was an easy one because I am familiar with the tech and how to handle it. Other options
are Neo4JS which I do not like. And

## Web API

I decided to stick with Django and Django Web Framework. I was learning both Django and Python and tackling GraphQL in
python seemed like a steep mountain for a small POC.

However I have used very little of what Django offers since my Database is actually stored in Janusgraph. The Django
power would be used further for Authentication over the Eve Api swell as serving views to an SPA.

## Test Suite

I stuck with Django testing. Seems to get the job well done and my unit tests were easy to set up and make work.

## Bonus SPA

As the project was time-consuming and ideally you would not create and SPA but reintegrate the answers back into the
game mechanics I have not done an SPA.