pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'spanneddrive')
gnome = import('gnome')

gnome.compile_resources('spanneddrive',
  'spanneddrive.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'spanneddrive.in',
  output: 'spanneddrive',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

spanneddrive_sources = [
  '__init__.py',
  'utility.py',
  'gconstants.py',
  'readwrite.py',
  'main.py',
  'window.py',
  'settings.py',
]

install_data(spanneddrive_sources, install_dir: moduledir)
