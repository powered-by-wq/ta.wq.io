import yaml
import json
import os, shutil
from glob import glob
import pystache
from wq.app.util.build import Builder
import uuid

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "template")
TAWQ_DIR = os.path.join(os.path.dirname(__file__), "assets")


def start(project_dir):
    shutil.copytree(TEMPLATE_DIR, project_dir)

def build(filename='tawq.yml'):
    config = yaml.load(file(filename))

    build_dir = config.get('dest', 'build')
    stage_dir = build_dir + '-src'

    version = config.get('version', '0.0.0')
    version += '-' + str(uuid.uuid4())[:6]

    # Create staging directory as copy of tawq js/css/html assets
    shutil.rmtree(stage_dir, ignore_errors=True)
    shutil.copytree(TAWQ_DIR, stage_dir)

    # Copy project assets and slide configurations to staging directory
    shutil.copytree('assets', os.path.join(stage_dir, 'assets'))
    shutil.copytree('slides', os.path.join(stage_dir, 'slides'))
    shutil.copytree('data', os.path.join(stage_dir, 'data'))
    os.chdir(stage_dir)

    # Create a module to include any custom JavaScript
    jsfiles = ['"%s"' % filename for filename in glob('assets/*.js')]
    module = 'require([%s]);' % ','.join(jsfiles)
    open('js/custom.js', 'w').write(module)

    # Create a css file to include any custom CSS
    cssfiles = ['@import url(../assets/%s.css);' for filename in glob('assets/*css')]
    module = '\n'.join(cssfiles)
    open('css/custom.css', 'w').write(module)

    # Reference any images in appcache
    images = []
    for img in ('png', 'jpg', 'svg'):
        images.extend(glob('assets/*.%s' % img))

    # Tweak app.build.json with updated configuraiton
    appconf = json.load(file('app.build.json'))
    appconf['appcache']['cache'].extend(images)
    appconf['optimize']['dir'] = os.path.join('..', build_dir)
    if config.get('optimize', False):
        del appconf['optimize']['optimize']

    json.dump(appconf, file('app.build.json', 'w'), indent=4)

    # Run index.html through pystache
    html = pystache.render(file('index.html').read(), config)
    file('index.html', 'w').write(html)

    builder = Builder(version)
    builder.build()
    
    if not config.get('keep-src', False):
        os.chdir('..')
        shutil.rmtree(stage_dir, ignore_errors=True)
