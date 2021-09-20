
# Barsky-Scrapper

Barsky is a tool to identify fake "reviews" rated on the dealerrater.com

## How it works

The top 3 most suspicious reviews are chosen by,

1 - Barsky-Scrapper first collects the 5 pages of reviews from dealerrater.com for the model McKaig Chevrolet Buick.

2 - Then starts Identifying super affectionate words in the following table and sum their score values:

| Keyword       | Score Value |
| -----------   | ----------- |
|experience     | 10          |
|cool           | 20          |
|nice           | 30          |
|helped         | 40          |
|great          | 40          |
|happy          | 50          |
|awesome        | 60          |
|amazing        | 60          |
|recommend      | 60          |
|best           | 90          |
|exceptional    | 100         |
|fantastic      | 100         |
|superb         | 100         |

3 - By the last to accomplish the analysis, the application collects the rating values from the deal in the following HTML section:

<img src="https://raw.githubusercontent.com/ramonlimaramos/barsky-scrapper/main/.github/ratings_section.png" />

And then with the rating value summed, executes the last sum with previously explained in step 2 Score Values total, delivering the final punctuation

4 - With this punctuation the application classify and named the reviews according to the following table:

| Score from | Score to |  Label      |
| ---------- | -------- | ----------- |
| 0          | 260      |  Neutral    |
| 261        | 320      |  Happy      |
| 321        | 370      |  Excited    |
| 371        | 400      |  Amazed     |
| 401        | 99999    |  Suspicious |
## Getting Started

### Dependencies

There are two ways of testing, executing, and debugging via local or docker is up to you to choose what's fit best in your environment

- Local: for (Testing / Executing / Debugging)
    * Python3.8 installed<br/>
      *(If you are running different python3 version consider change VIRTUALENV_ARGS in the files **Makefile** and **extras/makefiles/python.mk**)*

    * virtualenv globally installed
      ```shell
      python3 -m pip install virtualenv
      ```
      *(Note: execute this with the same python version that you are going to put in the Makefile VIRTUALENV_ARGS)<br/><br/>Why this boring things?<br/>The main reason for that is to compile the libs that this project are using, preventing from automatic lib updates and unsecure code from it.*

    * libpq-dev:
    ```shell
    sudo apt install libpq-dev
    ```
    * postgresql postgresql-contrib:<br/>
    (_This application is using pycog2 to generate mock models in the test library but the last version still not counting with models in the domain for main use in the database_)
    ```shell
    sudo apt install postgresql postgresql-contrib
    ```

- Docker: for (Testing / Executing / Debuging)
    * Only a docker instance running

### Installing

- Local:<br/>
    Getting in the project folder and just run "**make**" command<br/>
    *(Don't need to activate the python venv will automatically do it)*
    ```shell
    user:~/barsky-scrapper$ make
    ```
    *After install the dependencies make command it also brings the help sub-comand by default*

- Docker:<br/>
    section below
### Executing program

- Local:
    * Running Most Suspicious Reviews
    ```shell
    $ make local_suspicious
    ```

    * Running the API
    ```shell
    $ make local_api
    ```
    *Access: http://localhost:5000 for live documentation*

    * Tests
    ```shell
    $ make local_test
    ```

    * Lint
    ```shell
    $ make codestyle
    ```

    * Test coverage report
    ```shell
    $ make coverage
    ```

- Docker:
    * Running Most Suspicious Reviews
    ```shell
    $ make suspicious
    ```

    * Running the API
    ```shell
    $ make api
    ```
    *Access: http://localhost:5001 for live documentation*

    * Tests
    ```shell
    $ make test
    ```

## Authors

Contributors names and contact info

Ramon Ramos

## Version History

* 0.0.1
    * First Release
    * CLI Implementation
    * API Implementation

## Note

- Addicional Comments:<br/>
    * There are parts in the code where has commented as "TODOS", I'm planning to create a workflow to scrapes the pages in parallelism by background tasking using RABBITMQ as queueing and REDIS as backend result all of them managed by CELERY framework.<br/>
    This will enhance the performance in scrapping and it will avoid the timeout synchronous as is implemented right now.

    * Also it is necessary includes an debouncing logic over the API requisitions
