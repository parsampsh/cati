# Cati usage
to learn cati cli usage, read this file.

## help command
this command shows help:

```bash
cati help
```

also you can see help of a specify command:

```bash
cati help list
cati help remove
# ...
```

## pkg command
this command is for working with `.cati` packages.

#### pkg show
```bash
# showing packages
cati pkg show somepackage.cati
cati pkg show pkg1.cati /path/to/pkg2.cati # ...
```

Options:
- --files|-f: shows list of package files

#### pkg build
```bash
# building packages
cati pkg build package-dir/
cati pkg build package-dir1/ package-dir2/ # ...
```

Options:
- --output|-o: set package package output path

#### pkg install
```bash
# installing packages
sudo cati pkg install somepackage.cati
sudo cati pkg install pkg1.cati pkg2.cati # ...
```

## list command
this command shows list of packages

```bash
cati list
```

Options:
- --installed: only show installed packages list

## remove command
this command remove packages

```bash
cati remove pkg1
cati remove pkg1 pkg2 # ...
```