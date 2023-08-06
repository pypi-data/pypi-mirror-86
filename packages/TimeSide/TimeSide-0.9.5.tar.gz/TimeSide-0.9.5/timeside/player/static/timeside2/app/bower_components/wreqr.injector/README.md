Wreqr.Injector
==============

A really simple dependency injection based on `Backbone.Wreqr.RequestResponse`

This library add 3 methods to `Backbone.Wreqr.RequestResponse`, which ease dependency injection across multiple modules.

Usage
-----
This module is available as an IIFE or as an UMD module, which means that it should works on commonjs, AMD, or in browser loaded in a script tag.

It's only dependency is `Backbone.Wreqr.RequestResponse` which means that you must have also Backbone.

Docs
----
See the `docs` folder for more information and some examples.

API
---

### set(name, value)

Register a `value` with the key `name` in the dependency injector.

Returns a reference to itself enable chaining calls.

### get(name)

Retrieve a `value` with the key `name` in the dependency injector.

Returns the asked value or if not found will throw an error.

### req(name, args)

Get a reference to a `name` handler with optional `args` that will can be called on runtime.

Returns a function.

Before executing the handler it should be defined first or it will throw an error. The main idea behind `req` is to setup handler that will be defined at runtime.

The motivation behind this function is multiple:
 - to permit the removal of hard coded expression
 - to ease testing
 - to adapt parameterize behaviour
 - ...
