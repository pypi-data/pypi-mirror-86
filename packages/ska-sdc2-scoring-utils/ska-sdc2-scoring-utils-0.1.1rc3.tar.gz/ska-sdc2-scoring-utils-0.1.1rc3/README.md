# SDC2 Submission scripts

This package contains two CLI clients for interaction with the SDC2 scoring service.

These are:

- `sdc2-score` : A CLI client to the SDC2 scoring service for SDC2 participants for uploading and checking the status of submissions.
- `sdc2-score-admin`: A CLI client providing admin functions for the SDC2 scoring service.

Install with:

```console
pip install ska-sdc2-scoring-utils
```

## sdc2-score

Basic usage:

```console
sdc2-score [-h] [--verbose] {create-submission,get-submission,leaderboard} ...
```

### *Note:*

*A user account is required creating a submission. This can be either set*
*from the CLI flags when using the `create-submission` command or by setting*
*the enviroment variables:*

- *`SDC2_SCORER_USER`*
- *`SDC2_SCORER_PASSWORD`*

*(CLI flags override values in the enviroment variables)*

## sdc2-score-admin

Basic usage:

```console
sdc2-score-admin [-h] [--verbose] {list-groups,add-group,delete-group,list-users,add-user,delete-user} ...
```

This client app requires that the following enviroment variables are set:

- `SDC2_SCORER_ADMIN_USER`
- `SDC2_SCORER_ADMIN_PASSWORD`
