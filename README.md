# Fio
fīō (Verb - Latin) - I am made.

Kubernetes operators are a difficult field to enter into for some. It requires understanding of writing controllers, the Kubernetes API, CRDs, and sometimes working knowledge of Golang. Developers or operations often don't want to deal with the surrounding controller logic and code complexity of operators, instead they want to just focus on business logic for their automation. Likely, outside of Kubernetes, they already have a set of scripts or custom programs that capture this automation (such as the lifecycle scripts used to manage an Elasticsearch cluster on VMs - published by Elastic).

Fio attempts to lower this barrier to entry. Fio is designed to handle the controller logic and allow users to implement their business logic in any language, and for simple tasks no programming language at all. Fio is a task pipelining framework which enables users to describe complex workflows using declarative Kubernetes native objects.

Tasks are made of the following four plugin types (in this order): Triggers, Inputs, Transforms, and Outputs. Plugins create, enrich, modify, or read an event data structure. Tasks are declared with a Fio CRD object, and implemented by the Fio Kubernetes controller. Pipelines can be created by letting the output of one task trigger another task.

Here is an example task:

In plain english: In Kubernetes, add a sidecar to all deployments with services attached

**Trigger:** when new deployments are created. Triggers create the event data structure.

**Input:** query the Kubernetes API for all deployments and services. Inputs enrich the event data structure.

**Transform:** create a Kubernetes Job or serverless function to implement the following business logic, which modifies the event data structure:
- Identify deployments that are selected by services and don't already have the sidecar
- Enrich those deployment objects with a sidecar

**Outputs:** publish the changes back to the Kubernetes API. Outputs read and publish sections of the event data structure to external resources.

## Plugins
Plugins are executed in order. Conditional logic is also allowed to control the flow of plugins. For example, creating an event object only when a set of Triggers are all firing. Another example would be to only publish to an Output if certain fields exist on the event data structure.

Conditional logic:
- if/else
- and
- or
- not

## Triggers
Triggers create events. They also place information about what triggered the event on the event object.

Planned Triggers:
- Kubernetes API - polls the k8s API for specified object changes (Create, Update, Delete)
- Subscribe to message queue - listen for published messages on a topic
- Webhook - external sources can trigger an event
- Cron - trigger events on a schedule

## Inputs
Inputs enrich the event. These should be used to gather additional information not captured by the trigger. Ideally, information gathered will be used by a Transform or an Output.

Planned Inputs:
- Read the Kubernetes API - query to read Kubernetes API objects
- External API - query an external API for additional information
- Datastore - query an external database, file system, object storage, or version control

## Transforms
Transforms modify the event object. Transforms implement the business logic of the automation. Transforms receive the event data structure as input, execute the business logic, then the output enriches the event object.

Planned Transforms:
- Execute a Kubernetes Job - The event object is mounted as a secret. The business logic is executed with a user-specified container image. The output (TODO) will then enrich the event data structure.
- Serverless function - the event is the input, and the output enriches the event object
- Code Block - supply code directly in the Task object. Similar to the [Ruby filter plugin in Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-filters-ruby.html)
- Render a template. Templates and their values can be pulled by input plugins. These templates are then rendered by popular rendering engines, such as Jinja.

## Outputs
Outputs read a specified portion of the event object and publish that data to an external source.

Planned Outputs:
- Kubernetes API - create, update/apply, or delete API objects
- Publish to message queue - publish a message to a PubSub topic, which could be used to trigger another task
- Exec into a pod - run arbitrary commands inside pods
- External API - publish updates to an external API
- Datastore - publish to an external database, file system, or object storage
- STDOUT

## CRD Example
> Note: subject to change

In plain english: When a deployment is deleted, render templates to create new Kubernetes objects.

```yaml
apiVersion: fio.harmony-integrations.io/beta
kind: task
metadata:
  name: sample
  namespace: default
spec:
  triggers:
  - type: kubernetes
    config:
      delete: deployments
  inputs:
  - type: git
    eventField: templates
    config:
      repo: ssh://github.com/concordia-integrations/some-repo.git
      branch: main
  - type: bucket
    eventField: values
    config:
      bucket: https://bucket-name.s3.Region.amazonaws.com/keyname
  transforms:
  - type: jinja2
    eventField: renderedObjects
    config:
      templateField: templates
      valuesField: values
  outputs:
  - type: kubernetes
    config:
      applyField: renderedObjects
```

## Getting started:
TODO
