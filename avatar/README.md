# Todo
• set up good DNS website name for the EC2 instance

• see if you can create separate app that can bombard your
ec2 server with requests to eventually use in profile app.
Test it on avatar. Learn about getting access to (real-time?)
data about AWS EC2 load/performance

• learn / setup caching

# Roadmap
• profiler UI improvements:
    • fix request timer to run based on start time
    • add learn more modal to custom optimization
    • animate progress bar
    • ReactJsonView code split is creating server bundle 
    as well. Configure to only create client bundle
    
• Move db off same machine as server, use AWS service to host
db on cloud

• Move reactserver to separate microservice

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

• work through progressively newer back end system 
architectures. Keep them all to eventually create system
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

• profile app that can AB test and profile performance of
this site's history of different system architectures 
in real time with UI that allows user to configure which 
setup to use, generates artificial system load, and
profiles results with some kind of visuals. Examples
of systems to test:
[
  • SSR vs SPA
  • single webserver vs distributed
  • redis cache
  • hosted server vs serverless
]

• react-three-fiber and react-spring for banner animations

• graphql - use it on detail page

• chat app with chat bots (maybe with ML) talking to each
other to generate large database of conversations that user
can access

• avatar...
