# Todo
• work on environment variables (Python decouple, using
.env file instead of REACTSERVER_ENV method)
• consider implementations for persisting SPA state through
refreshes (localStorage, cookies, external session manager
like redis)

# Roadmap
• see if you can create separate app that can bombard your
ec2 server with requests to eventually use in profile app

• portfolio home page is list of large, full width banners
representing individual parts of my portfolio that will 
eventually have a cool 3d or 2d animation in each banner

• portfolio home list: 
[
  participation reports,
  cryptograf,
  knovigator?,
  portfolio: [discussion of evolving tech and profiler]
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

• chat app with chat bots (maybe with ML) talking to each
other to generate large database of conversations that user
can access

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

• avatar...
