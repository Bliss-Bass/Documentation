# Contributing to Bass OS

We are not going to require any elitist rules for you to contribute to the project. That's just silly. So this doc will cover the various parts of the project and explain how to do things. 

## General Development

This project contains many scripts and tools that help aid the support, feature selection, and option customization for Bass OS. Most of those scripts use bash and can also interface with the easy-menu-system we include. 

## Addon Development

Pick the guide that matches your tree. They are not interchangeable.

| Product | Guide |
|---------|--------|
| **Bass: Lineout** (`vendor/ax86-lite`) | [Addon Development: Bass Lineout](addon-development.md) |
| **Classic Bass OS** (`private/addons/`, unfold) | [Addon Development: Legacy Bass OS](addon-development-legacy-bass.md) |

**Lineout:** new apps and services go in `vendor_packages/` with a product makefile and a `build.sh` flag. Runtime `/data/misc` overrides use `addon_init` (same Lineout guide).

**Legacy Bass:** patchsets and private manifests go under `private/addons/` for unfold. That path is not how Lineout adds packages.

## Documentation

When you add a Lineout package, put a `README.md` next to the code so [Ax86Docs](../applications/Ax86Docs/Ax86Docs.md) can pick it up, and add or update a page under this Documentation repo when the feature is user- or OEM-facing.
