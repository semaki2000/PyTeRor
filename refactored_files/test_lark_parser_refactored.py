import os
from textwrap import dedent
import pytest
from ert.config.parsing import ConfigValidationError, init_user_config_schema, lark_parse

def touch(filename):
    with open(filename, 'w', encoding='utf-8') as fh:
        fh.write(' ')

@pytest.mark.usefixtures('use_tmpdir')
def test_that_missing_arglist_does_not_affect_subsequent_calls():
    """
    Check that the summary without arglist causes a ConfigValidationError and
    not an error from appending to None parsed from SUMMARY w/o arglist
    """
    with open('config.ert', mode='w', encoding='utf-8') as fh:
        fh.write(dedent("""
                NUM_REALIZATIONS 1
                SUMMARY
                SUMMARY B 2
                """))
    with pytest.raises(ConfigValidationError, match='must have at least'):
        _ = lark_parse('config.ert', schema=init_user_config_schema())

@pytest.mark.usefixtures('use_tmpdir')
def test_that_setenv_does_not_expand_envvar():
    with open('config.ert', mode='w', encoding='utf-8') as fh:
        fh.write(dedent("""
                NUM_REALIZATIONS 1
                SETENV PATH $PATH:added
                """))
    config = lark_parse('config.ert', schema=init_user_config_schema())
    assert config['SETENV'] == [['PATH', '$PATH:added']]

@pytest.mark.usefixtures('use_tmpdir')
def test_that_realisation_is_a_alias_of_realization():
    with open('config.ert', mode='w', encoding='utf-8') as fh:
        fh.write(dedent("""
                NUM_REALISATIONS 1
                """))
    config = lark_parse('config.ert', schema=init_user_config_schema())
    assert config['NUM_REALIZATIONS'] == 1

@pytest.mark.usefixtures('use_tmpdir')
def test_that_redefines_are_applied_correctly_as_forward_model_args():
    test_config_file_name = 'test.ert'
    test_config_contents = dedent("""
        NUM_REALIZATIONS  1
        DEFINE <A> 2
        DEFINE <B> 5
        FORWARD_MODEL MAKE_SYMLINK(<U>=<A>, <F>=<B>, <E>=<O>, R=Hello, <R>=R)
        DEFINE <B> 10
        DEFINE B <A>
        DEFINE D <A>
        DEFINE <A> 3
        FORWARD_MODEL MAKE_SYMLINK(<U>=<A>, <D>=B)
        DEFINE B <A>
        DEFINE C <A>

        """)
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_config_contents)
    config_dict = lark_parse(file=test_config_file_name, schema=init_user_config_schema())
    defines = config_dict['DEFINE']
    assert ['<A>', '2'] not in defines
    assert ['<B>', '2'] not in defines
    assert ['<A>', '3'] in defines
    assert ['D', '2'] in defines
    assert ['B', '3'] in defines
    assert ['C', '3'] in defines

def test_include_non_existing_file(tmpdir):
    with tmpdir.as_cwd():
        config = """
        JOBNAME my_name%d
        NUM_REALIZATIONS 1
        INCLUDE does_not_exists
        """
        with open('config.ert', mode='w', encoding='utf-8') as fh:
            fh.writelines(config)
        with pytest.raises(ConfigValidationError, match='INCLUDE file:.*does_not_exists not found'):
            _ = lark_parse('config.ert', schema=init_user_config_schema())

def test_invalid_user_config():
    with pytest.raises(FileNotFoundError):
        _ = lark_parse('this/is/not/a/file', schema=init_user_config_schema())

def test_that_unknown_queue_option_gives_error_message(tmp_path):
    test_user_config = tmp_path / 'user_config.ert'
    test_user_config.write_text('QUEUE_OPTION UNKNOWN_QUEUE unsetoption')
    with pytest.raises(ConfigValidationError, match="'QUEUE_OPTION' argument 1 must be one of"):
        _ = lark_parse(str(test_user_config), schema=init_user_config_schema())

@pytest.mark.usefixtures('use_tmpdir')
def test_include_cyclical_raises_error():
    test_config_file_name = 'test.ert'
    test_config_self_include = """NUM_REALIZATIONS  1
INCLUDE test.ert
"""
    test_config_contents = """NUM_REALIZATIONS  1
INCLUDE include.ert
"""
    test_include_file_name = 'include.ert'
    test_include_contents = """JOBNAME included
INCLUDE test.ert
"""
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_config_contents)
    with open(test_include_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_include_contents)
    with pytest.raises(ConfigValidationError, match='Cyclical .*test.ert'):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_config_self_include)
    with pytest.raises(ConfigValidationError, match='Cyclical .*test.ert->test.ert'):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())

@pytest.mark.parametrize('parametrizedvar0, parametrizedvar1', [("""
        NUM_REALIZATIONS  1
        QUEUE_OPTION VOCAL MAX_RUNNING 50
        """, 'VOCAL'), ("""
        NUM_REALIZATIONS  hello
        """, 'integer'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA  hello
        """, 'number'), ("""
        NUM_REALIZATIONS  1
        STOP_LONG_RUNNING NOT_YES
        """, 'boolean'), ("""
        NUM_REALIZATIONS  1
        JOB_SCRIPT  hello
        """, 'executable'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA
        """, 'at least 1 arguments'), ("""
        NUM_REALIZATIONS  1
        ENKF_ALPHA 1.0 2.0 3.0
        """, 'maximum 1 arguments')])
@pytest.mark.usefixtures('use_tmpdir')
def test_that_giving_incorrect_queue_name_in_queue_option_fails_parameterized(parametrizedvar0, parametrizedvar1):
    test_config_file_name = 'test.ert'
    test_config_contents = dedent(parametrizedvar0)
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write(test_config_contents)
    with pytest.raises(ConfigValidationError, match=parametrizedvar1):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())

@pytest.mark.usefixtures('use_tmpdir')
def test_that_giving_no_keywords_fails_gracefully():
    test_config_file_name = 'test.ert'
    with open(test_config_file_name, 'w', encoding='utf-8') as fh:
        fh.write('')
    with pytest.raises(ConfigValidationError, match='must be set'):
        _ = lark_parse(test_config_file_name, schema=init_user_config_schema())

def test_num_realizations_required_in_config_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config_file_name = 'config.ert'
    config_file_contents = 'ENSPATH storage'
    with open(config_file_name, mode='w', encoding='utf-8') as fh:
        fh.write(config_file_contents)
    with pytest.raises(ConfigValidationError, match='NUM_REALIZATIONS must be set.*'):
        _ = lark_parse(config_file_name, schema=init_user_config_schema())

@pytest.mark.usefixtures('use_tmpdir')
def test_not_executable_job_script_fails_gracefully():
    """Given a non executable job script, we should fail gracefully"""
    config_file_name = 'config.ert'
    script_name = 'not-executable-script.py'
    touch(script_name)
    config_file_contents = dedent(f'NUM_REALIZATIONS 1\n         JOB_SCRIPT {script_name}\n         ')
    with open(config_file_name, mode='w', encoding='utf-8') as fh:
        fh.write(config_file_contents)
    with pytest.raises(ConfigValidationError, match=f'not executable.*{script_name}'):
        _ = lark_parse(config_file_name, schema=init_user_config_schema())

@pytest.mark.usefixtures('use_tmpdir')
def test_not_executable_job_script_somewhere_in_PATH_fails_gracefully(monkeypatch):
    """Given a non executable job script referred to by relative path (in this case:
    just the filename) in the config file, where the relative path is not relative to
    the location of the config file / current directory, but rather some location
    specified by the env var PATH, we should fail gracefully"""
    config_file_name = 'config.ert'
    script_name = 'not-executable-script.py'
    path_location = os.path.join(os.getcwd(), 'bin')
    os.mkdir(path_location)
    touch(os.path.join(path_location, script_name))
    os.chmod(path_location, 0)
    monkeypatch.setenv('PATH', path_location, ':')
    config_file_contents = dedent(f'NUM_REALIZATIONS 1\n         JOB_SCRIPT {script_name}\n         ')
    with open(config_file_name, mode='w', encoding='utf-8') as fh:
        fh.write(config_file_contents)
    with pytest.raises(ConfigValidationError, match='Could not find executable'):
        _ = lark_parse(config_file_name, schema=init_user_config_schema())
    os.chmod(path_location, 1909)