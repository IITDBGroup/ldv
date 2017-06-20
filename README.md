# ldv

A tool for lightweight database application virtualization. Light-weight database virtualization (LDV) is a novel approach for sharing and repeating applications that use a relational database. LDV monitors a DB application to create a repeatability package that encapsulates the application and its dependencies (input files, binaries, and libraries) as well as the necessary and relevant data from the database required for successful repetition. LDV relies on data provenance to determine which database tuples and input files are relevant. While monitoring an application to create a package we incrementally construct an execution trace (provenance graph), that records dependencies across OS and DB boundaries. Such a package can be shared and reexecuted on any compatible machine without requiring installation of dependencies (e.g., database system or libraries) and without having to manually create and setup a database.

## Monitoring Applications


To use our LDV system, the user monitors an execution by prefixing the command starting the application with ldv-audit:

~~~
ldv-audit run-dbapp
~~~

The figure below shows how LDV monitors the execution of the user's application and its interactions with the OS and DB system. By intercepting system calls such as file operations and process creation as well as SQL statements send to the DB we incrementally build what we call an execution trace - a provenance graph that records both OS and DB operations and data dependencies. In addition to creating the execution traces and including it in the reproducibility package for the application, LDV also copies accessed files and database tuples into the package. We support two options for shipping the database. The <i>server-include</i> packaging option includes a DB server and the relevant DB slice in the package. The <i>server-excluded</i> packaging option captures the results to queries issued by the application and stores these query results in the package.


<embed src="../images/ldv_monitor.svg" type="image/svg+xml" class="aligncenter" height="250"  width="620"/>



## Sharing and Reexecution


To replay the execution of an application stored in a package, without any installation or configuration, the user issues for a shared package:

`ldv-exec run-dbapp`

Before starting the actual application, LDV will start-up the database server included in the package, create the schema of the application, and load the DB slice. During application execution we reroute SQL queries to the package database and file operations into the package. If the server-excluded packaging option was chosen then we replay query results included in the package from files instead of actually executing any SQL operations.


<embed src="../images/ldv_reexec.svg" type="image/svg+xml" class="aligncenter" height="250"  width="620"/>


<!-- ************************************************************ -->
## Contributors

* <a href="http://www.ci.anl.gov/profile/252" target="_new">Tanu Malik</a> - Research Associate at the University of Chicago, Computation Institute and Argonne National Labs
* <a href="https://au.linkedin.com/pub/tran-quan-pham/b3/19/657" target="_new">Quan Pham</a> - Ph.D. Student at the University of Chicago (graduated)
* <a href="http://webservices.uchicago.edu/about/staff/richard_whaling/" target="_new">Richard Whaling</a> - Emerging Technologies Developer at the University of Chicago
* <a href="http://www.ci.anl.gov/profile/252" target="_new">Ian Foster</a> - University of Chicago, Director Computation Institute


