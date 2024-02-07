"""File used to test whether changes to NiCad's Python grammar work in removing 
the possibility of recognizing f-strings and string literals as the same node."""

#@pytest.mark.parametrize("kw", REPLACE_WITH_GEN_KW)
def test_that_suggester_gives_gen_kw_migrations(tmp_path, kw):
    (tmp_path / "config.ert").write_text(f"NUM_REALIZATIONS 1\n{kw}\n")
    suggestions = make_suggestion_list(str(tmp_path / "config.ert"))

    assert any(
        "ert.readthedocs.io/en/latest/reference/configuration/keywords.html#gen-kw" in s
        for s in suggestions
    )


#@pytest.mark.parametrize("kw", RSH_KEYWORDS)
def test_that_suggester_gives_rsh_migrations(tmp_path, kw):
    (tmp_path / "config.ert").write_text(f"NUM_REALIZATIONS 1\n{kw}\n")
    suggestions = make_suggestion_list(str(tmp_path / "config.ert"))

    assert any(
        "deprecated and removed support for RSH queues." in s for s in suggestions
    )


#@pytest.mark.parametrize("kw", USE_QUEUE_OPTION)
def test_that_suggester_gives_queue_option_migrations(tmp_path, kw):
    (tmp_path / "config.ert").write_text(f"NUM_REALIZATIONS 1\n{kw}\n")
    suggestions = make_suggestion_list(str(tmp_path / "config.ert"))

    assert any(
        f"The {kw} keyword has been removed. For most cases " in s for s in suggestions
    )