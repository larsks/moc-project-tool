# MOC Project Tool

This is an Ansbile project that reads project descriptions from a
collection of YAML files and uses that information to create projects,
quotas, and groups in OpenShift.

## Requirements

You will need the `kubernetes.core` collection to run this playbook.
To install the necessary requirements:

```
ansible-galaxy install -r requirements.yaml
```

## Quotas

Quotas are defined in the `quotas/` directory in
`quota/<quotaname>/resourcequota.yaml`. All quotas should be named
`default`, with their descriptive name store in the
`massopen.cloud/quota-name` annotation, like this:

```

kind: ResourceQuota
apiVersion: v1
metadata:
  name: default
  annotations:
    massopen.cloud/quota-name: "x-small"
spec:
  hard:
    requests.cpu: '500m'
    requests.memory: 2Gi
    limits.cpu: '500m'
    limits.memory: 2Gi
    requests.storage: 10Gi
```

This makes it easy to update quotas for an existing project.

If you add additional quotas to this repository, also update the JSON
schema in the [moc-openshift-projects][] repository.

[moc-openshift-projects]: https://github.com/CCI-MOC/moc-openshift-projects

## See also

The Kubernetes documentation:

- [Resource quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
- [Resource requests and limits of Pod and
  Container](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

These third-party articles:

- [Kubernetes best practices: Resource requests and
  limits](https://cloud.google.com/blog/products/containers-kubernetes/kubernetes-best-practices-resource-requests-and-limits)
