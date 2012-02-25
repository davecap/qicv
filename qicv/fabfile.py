from fabric.api import cd, env, prefix, run, sudo, local, settings, roles
from contextlib import contextmanager
import subprocess
import os
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

env.roledefs = {
}

env.root_dir = os.path.dirname(os.path.abspath(__file__))
env.virtualenv = env.root_dir + '/env'
env.code_dir = os.path.join(env.root_dir, 'qicv')
env.activate = 'source %s/bin/activate ' % env.virtualenv
env.media_dir = '%s/media' % env.code_dir

#
# Helpers
#


@contextmanager
def _virtualenv():
    with prefix(env.activate):
        yield


def _call_command(command):
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()

#
# General tasks
#


def update_requirements():
    """ update external dependencies on remote host """
    with cd(env.root_dir):
        with _virtualenv():
            run('pip install -r requirements.txt')

#
# Local tasks
#


def assert_git_latest():
    """
    Check git repo to make sure it is ready to deploy the latest code
    """

    branch = 'master'
    out, err = _call_command('git status')

    if not out.startswith('# On branch %s' % branch):
        raise Exception('You must be in %s to deploy' % branch)
    else:
        logging.info('In %s branch' % branch)

    if not out.endswith('nothing to commit (working directory clean)\n'):
        raise Exception('Directory not clean, you must commit:\n%s' % out)
    else:
        logging.info('Directory clean')

    out, err = _call_command('git push --dry-run')
    if err == 'Everything up-to-date\n':
        logging.info('Remote repository up to date')
    else:
        raise Exception('Remote repository was not up to date:\n%s' % err)

    out, err = _call_command('git pull')
    if 'up-to-date' not in out:
        raise Exception('Local copy was not up to date:\n%s' % out)
    else:
        logging.info('Local copy up to date')


def assert_db_valid():
    """
    Run validate to ensure that the schema is valid.
    """
    with cd(env.root_dir):
        with _virtualenv():
            out, err = _call_command('python %(code_dir)s/manage.py validate' % env)
            try:
                line = [l for l in out.split('\n') if l.strip()][0]
            except:
                raise Exception('DB schema not valid!')
            if not line.startswith('0 errors found'):
                raise Exception('DB schema not valid!')
    logging.info('DB schema valid!')


def assert_static_latest():
    """
    Assert that we have the latest static files in STATIC_ROOT
    """
    out, err = _call_command('python %(code_dir)s/manage.py collectstatic -i "*.pyc" --noinput -n' % env)
    # there should only be 1 line with text in it... so get that line
    try:
        line = [l for l in out.split('\n') if l.strip()][0]
    except:
        raise Exception('Staticfiles not up-to-date. Run fab collectstatic and push.')
    if not line.startswith('0 static files copied'):
        raise Exception('Staticfiles not up-to-date. Run fab collectstatic and push.')
    logging.info('Staticfiles up-to-date!')


def collectstatic(static_root='static_root'):
    static_root = os.path.join(env.code_dir, static_root)
    if not os.path.exists(static_root):
        logging.info('Creating STATIC_ROOT: %s' % static_root)
        os.mkdir(static_root)
    local('python %(code_dir)s/manage.py collectstatic -i "*.pyc" --noinput' % env)


def static():
    local('make')
    collectstatic()


def runserver(port='8080'):
    with cd(env.root_dir):
        with _virtualenv():
            env.server_port = port
            local('python %(code_dir)s/manage.py runserver %(server_port)s --verbosity=2' % env, capture=False)


def syncdb():
    with cd(env.root_dir):
        with _virtualenv():
            local('python %(code_dir)s/manage.py syncdb --noinput' % env, capture=False)


def initialmigration(app):
    assert_db_valid()
    with cd(env.root_dir):
        with _virtualenv():
            env.app = app
            local('python %(code_dir)s/manage.py schemamigration %(app)s --initial' % env, capture=False)


def schemamigration(app):
    assert_db_valid()
    with cd(env.root_dir):
        with _virtualenv():
            env.app = app
            local('python %(code_dir)s/manage.py schemamigration %(app)s --auto' % env, capture=False)


def migrate(app=None):
    assert_db_valid()
    with cd(env.root_dir):
        with _virtualenv():
            env.app = app
            if app:
                local('python %(code_dir)s/manage.py migrate %(app)s' % env, capture=False)
            else:
                local('python %(code_dir)s/manage.py migrate' % env, capture=False)


def makemessages(locale=None):
    with cd(env.root_dir):
        with _virtualenv():
            if locale:
                local('python %(code_dir)s/manage.py makemessages -l %s' % (env, locale), capture=False)
            else:
                local('python %(code_dir)s/manage.py makemessages -a' % env, capture=False)
    logging.info('Now run compilemessages.')


def compilemessages():
    with cd(env.root_dir):
        with _virtualenv():
            local('python %(code_dir)s/manage.py compilemessages' % env, capture=False)


def test():
    with cd(env.root_dir):
        with _virtualenv():
            local('python %(code_dir)s/manage.py test --settings="dolbeau.settings_test"' % env, capture=False)


def clean():
    """
    Remove all .pyc files
    """
    local('find . -name "*.pyc" -exec rm {} \;')


# @roles('production')
# def deploy():
#     """
#     Push code, sync, migrate, generate media, restart
#     """
#     assert_git_latest()
#     #assert_static_latest()
#     production()
#     with cd(env.root_dir):
#         with _virtualenv():
#             provision()
#             #sudo('python %(code_dir)s/manage.py syncdb --noinput' % env, pty=True)
#             #sudo('python %(code_dir)s/manage.py migrate' % env, pty=True)
#             # run('python %(code_dir)s/manage.py compress --force' % env, pty=True)
