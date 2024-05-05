import datetime
import json
import os
import pandas
import requests
import settings
import warnings

def read_dataset(id, **params):


    # Parameters ----

    id = id if isinstance(id, (list, tuple)) else [id]
    if "username" in params and "password" in params:
        credentials = params["username"] + ";" + params["password"]
    elif "ECONDATA_CREDENTIALS" in os.environ:
        credentials = os.environ["ECONDATA_CREDENTIALS"]
    else:
        raise Exception("No credentials supplied")
    if "agencyid" in params:
        x = params["agencyid"]
        agencyid = x if isinstance(x, (list, tuple)) else [x]
    else:
        agencyid = ["ECONDATA"]
    if "version" in params:
        x = params["version"]
        version = x if isinstance(x, (list, tuple)) else [x]
    else:
        version = ["latest"]
    env = settings.EconData()


    # Fetch data set(s) ----

    print("Fetching dataset(s) - " + ", ".join(id) + "\n")
    session = requests.Session()
    if "file" in params:
        with open(params["file"]) as file:
            data_message = json.load(file)
        print("Data set(s) successfully retrieved from local storage.\n")
    else:
        [username, password] = credentials.split(";")
        session.post(env.url + "/signin",
                     data = {"username": username,
                             "password": password})
        query_params = {"agencyids": ",".join(agencyid),
                        "ids": ",".join(id),
                        "versions": ",".join(version)}
        response = session.get(env.url + "/" + env.path + "/datasets",
                               params = query_params)
        if not response.ok:
            raise Exception(response.json())
        data_message = response.json()
    data_sets = data_message[1]["data-sets"]
    database = [process_dataset(env, session, x, params) for x in data_sets]
    if len(database) == 1:
        return database[0]
    else:
        return database

def process_dataset(env, session, x, params):
    if "file" in params:
        tmp_data_set = x[1]
    else:
        data_set_ref = "-".join([x[1]["agencyid"],
                                 x[1]["id"],
                                 x[1]["version"]])
        query_params = {"release": get_release()}
        if "series-key" in params:
            query_params["series-key"] = params["series-key"]
        tmp_data_set = get_data(env, session, data_set_ref, query_params)
    data_set = [process_series(x) for x in tmp_data_set["series"]]
    return data_set

def get_release():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def get_data(env, session, ref, params, **kwargs):
    if "links" not in kwargs:
        response = session.get(env.url + "/" + env.path + "/datasets/" + ref,
                               params = params)
        if response.ok:
            print("Processing data set: " + ref + "\n")
        else:
            raise Exception(response.json())
        links = response.links
        data_message = response.json()
        data_set = data_message[1]["data-sets"][0][1]
        if "next" not in response.links:
            return data_set
        else:
            return get_data(env, session, ref, params,
                            links = links, data_set = data_set)
    else:
        response = session.get(env.url + "/" + kwargs["links"]["next"]["url"],
                               params = params)
        if response.ok:
            print("Processing data set: " + ref + "\n")
        else:
            raise Exception(response.json())
        links = response.links
        data_message = response.json()
        data_set = kwargs["data_set"]
        data_set["series"] = data_set["series"] + \
                data_message[1]["data-sets"][0][1]["series"]
        if "next" not in response.links:
            return data_set
        else:
            return get_data(env, session, ref, params,
                            links = links, data_set = data_set)

def process_series(x):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        series = pandas.DataFrame(x.pop("obs"))
        series.metadata = x
        return series
