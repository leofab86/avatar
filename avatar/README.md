# Todo
• Set up skeleton of profile app that allows creation of 
database table sets associated with current session. Each
session would have Teachers, Classes, Students. User can
select how many of each to model system complexity

• fill out db profile creation to generate random names

• Solve the django ORM query problem

• set up django_toolbar to show in prod

• see if you can create separate app that can bombard your
ec2 server with requests to eventually use in profile app

# Roadmap
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
  • multiple replicated database instances? (ask Tony)
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
