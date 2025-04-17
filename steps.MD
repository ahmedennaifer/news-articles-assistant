Notes:
  -  Metrics, baseline, important.
  -  rag+ tools.
  -  Vrai dataset, réponse attendue, metric on retrieval, and exact passage of answer. use case where the agent says “idk”
  -  Rapport d’avancement (échecs, erreur, etc)
  -  Pas uniquement du prompt engineering
Idea:
  - rag + tool use + routing based on specific collection.
  - tools:
    - db connector 
    - ... 

Needs:
  - ask question 
  - question gets routed to categories
  - ie: rag, db, general, make stuff. 
  - if make stuff:
    - acces to other tools: get_weather, get_current_time, get_flight, book_stuff, tbd.
  if db:
    - db tool, query stuff


Todo: 
  [ ] - Get Basic rag with routing 
    [X] - Custom routing component 
    [ ] - Connect routed query to relevant actor
  [ ] - Setup baseline + mrr 
  [ ] - Make processing step better  
  [ ] - Write few tools
