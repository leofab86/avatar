# Todo
• Build a ui for the load test app

• learn / setup caching

• Move reactserver to separate microservice

• Move db off same machine as server, use AWS service to host
db on cloud (will probably just create a separate EC2 for that
because RDS is expensive, or Aurora)

• Set up db and reactserver microservices in VPC. (Add
logging to them using server timing?)

# Roadmap
• profiler UI improvements:
    • fix request timer to run based on start time
    • add learn more modal to custom optimization and
    prefetch related, change generic description of 
    optimizations
    • animate progress bar
    • ReactJsonView code split is creating server bundle 
    as well. Configure to only create client bundle
    
• django code improvements:
    • change timing logging to a middleware that writes
    timing data to server timing api header
    
• work through progressively newer back end system 
architectures. Keep them all to create system
profiling app: 
[
  • ec2 hosting webserver, AWS RDS for DB, session
  management with Django or on DB
  • add service that spins up multiple webservers as
  necessary and load balancer to manage them and some 
  way to artificially test load on it
  • add redis for cache 
  • wrapping previous implementation in docker
  • serverless architecture
]

• profiler app that can AB test and profile performance of
this site's history of different system architectures 
in real time with UI that allows user to configure which 
setup to use, generates artificial system load, and
profiles results with some kind of visuals. Examples
of systems to test:
[
  • SSR vs SPA
  • single webserver vs auto scaling vs load balancer
  • with or without redis cache, possibly allow config for
  different caching strategies
  • hosted django vs serverless (ec2 vs fargate vs lambda)
]

• profiler app requires login. After login, programatically start
the ec2 instances necessary for the profiler app so that each user
has their own playground

• set up good DNS website name for the Django web server

• portfolio home page is list of large, full width banners
representing individual parts of my portfolio that will 
eventually have a cool 3d or 2d animation in each banner

• portfolio home list: 
[
  participation reports,
  cryptograf,
  knovigator?,
  profiler
]

• react-three-fiber and react-spring for banner animations

• graphql - use it on detail page?

• chat app with chat bots (maybe with ML) talking to each
other to generate large database of conversations that user
can access

• avatar...
