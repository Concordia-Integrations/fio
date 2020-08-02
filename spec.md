# Fio Task
Runs as a k8s operator. Listen to the k8s API for updates. Query data sources for more information. Transform data. Output data (such as update to k8s API)

## Trigger (API object changes)
* Object CRUD (even CRDs)
* Change in objects found by selector
* Change in objects by targetRef
* Cron
* Webhook

## Inputs (data fields to pull in and from where)
- all inputs are mapped to a user provided field name
- can set to root event

* Object selector
* Object targetRef
* Changed field names (could use lookup of previously applied config in annotations)
* JSON path query
* pull from external API

## Transform (manipulations of data)
* filters
* Logic (and, or, if, while, etc)
* Run k8s Job (inputs as env vars, use base image, provide script, scrape outputs (get added to the list of variables on the procedure)
  1. expose all vars as JSON object. Mounted with a k8s secret
  1. k8s job is created (assumed that execution of the container knows how to use the input file)
  1. STDOUT contains a JSON object. Other text can be outputted, but first JSON object detected will become the new event object.

## Outputs (set data)
* CRUD object
* Call external API
