import types
from pathlib import Path
from unittest.mock import call

import pytest
from pytest_mock import MockerFixture

from numfile import NumberedFile, open_all, open_latest, open_next


class TestNumberedFileOf:
    def test_should_accept_str_or_path(self):
        assert NumberedFile.of("file") == NumberedFile.of(Path("file"))

    def test_should_return_numbered_file(self):
        assert isinstance(NumberedFile.of("/path/to/file"), NumberedFile)

    def test_should_parse_no_path(self):
        file = NumberedFile.of("file")
        assert file.parent == Path(".")

    def test_should_parse_relative_path(self):
        file = NumberedFile.of("path/to/file")
        assert file.parent == Path("path/to/")

    def test_should_parse_absolute_path(self):
        file = NumberedFile.of("/path/to/file")
        assert file.parent == Path("/path/to")

    def test_should_parse_plain_name(self):
        file = NumberedFile.of("/path/to/file")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number is None
        assert file.suffix == ""

    def test_should_parse_simple_suffix(self):
        file = NumberedFile.of("/path/to/file.txt")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number is None
        assert file.suffix == ".txt"

    def test_should_parse_complex_suffix(self):
        file = NumberedFile.of("/path/to/file.txt.tar.gz")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number is None
        assert file.suffix == ".txt.tar.gz"

    def test_should_parse_number(self):
        file = NumberedFile.of("/path/to/file-42")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number == 42
        assert file.suffix == ""

    def test_should_parse_number_and_simple_suffix(self):
        file = NumberedFile.of("/path/to/file-42.txt")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number == 42
        assert file.suffix == ".txt"

    def test_should_parse_number_and_complex_suffix(self):
        file = NumberedFile.of("/path/to/file-42.txt.tar.gz")
        assert file.parent == Path("/path/to")
        assert file.name == "file"
        assert file.number == 42
        assert file.suffix == ".txt.tar.gz"


class TestCurrentPath:
    @pytest.mark.parametrize(
        "path",
        [
            "/path/to/file",
            "/path/to/file.txt",
            "/path/to/file.txt.tar.gz",
            "/path/to/file-42",
            "/path/to/file-42.txt",
            "/path/to/file-42.txt.tar.gz",
        ],
    )
    def test_should_return_path_instance(self, path: str):
        file = NumberedFile.of(path)
        assert isinstance(file.path, Path)

    @pytest.mark.parametrize(
        "path",
        [
            "/path/to/file",
            "/path/to/file.txt",
            "/path/to/file.txt.tar.gz",
        ],
    )
    def test_should_parse_path_without_number(self, path: str):
        file = NumberedFile.of(path)
        assert file.path == Path(path)

    @pytest.mark.parametrize(
        "path",
        [
            "/path/to/file-42",
            "/path/to/file-42.txt",
            "/path/to/file-42.txt.tar.gz",
        ],
    )
    def test_should_parse_path_with_number(self, path: str):
        file = NumberedFile.of(path)
        assert file.path == Path(path)


class TestNext:
    def test_should_return_numbered_file(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        assert isinstance(file.next, NumberedFile)

    def test_no_latest_and_no_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, False])
        file = NumberedFile.of("/path/to/no-such-file")
        assert file.next == NumberedFile.of("/path/to/no-such-file-1")

    def test_no_latest_but_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, False])
        file = NumberedFile.of("/path/to/no-such-file-42")
        assert file.next == NumberedFile.of("/path/to/no-such-file-42")

    def test_latest_without_number_and_no_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, True])
        file = NumberedFile.of("/path/to/foobar")
        assert file.next == NumberedFile.of("/path/to/foobar-2")

    def test_latest_without_number_but_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, True])
        file = NumberedFile.of("/path/to/foobar-42")
        assert file.next == NumberedFile.of("/path/to/foobar-2")

    def test_latest_with_number_but_no_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, True])
        file = NumberedFile.of("/path/to/foo")
        assert file.next == NumberedFile.of("/path/to/foo-3")

    def test_latest_with_number_and_number_given(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch.object(Path, "exists", side_effect=[True, True])
        file = NumberedFile.of("/path/to/foo-42")
        assert file.next == NumberedFile.of("/path/to/foo-3")


class TestLatest:
    def test_should_return_numbered_file(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        assert isinstance(file.latest, NumberedFile)

    def test_should_return_self_if_no_such_file(self, fake_files):
        file = NumberedFile.of("/path/to/no-such-file")
        assert file.latest is file

    def test_should_return_file_with_highest_number(self, fake_files):
        file = NumberedFile.of("/path/to/ipsum")
        assert file.latest.path == Path("/path/to/ipsum-12")

    def test_should_ignore_given_number(self, fake_files):
        file = NumberedFile.of("/path/to/ipsum-42")
        assert file.latest.path == Path("/path/to/ipsum-12")


@pytest.fixture
def fake_files(mocker: MockerFixture) -> None:
    mocker.patch.object(Path, "exists", return_value=True)
    mocker.patch.object(
        Path,
        "iterdir",
        return_value=[

            # Unrelated files
            Path("/path/to/__init__.py"),
            Path("/path/to/main.py"),
            Path("/path/to/utils.py"),

            # Same name but different suffixes
            Path("/path/to/foo"),
            Path("/path/to/foo.md"),
            Path("/path/to/foo.txt"),
            Path("/path/to/foo.txt.tar.gz"),

            # Name prefix shared with other files
            Path("/path/to/foobar"),
            Path("/path/to/foobar.md"),
            Path("/path/to/foobar.txt"),
            Path("/path/to/foobar.txt.tar.gz"),

            # Plain with numbers
            Path("/path/to/file-1"),
            Path("/path/to/file-2"),
            Path("/path/to/file-3"),
            Path("/path/to/file-4"),

            # Plain starting with no number
            Path("/path/to/lorem"),
            Path("/path/to/lorem-2"),
            Path("/path/to/lorem-3"),

            # Gaps
            Path("/path/to/ipsum-3"),
            Path("/path/to/ipsum-8"),
            Path("/path/to/ipsum-9"),
            Path("/path/to/ipsum-12"),

            # Numbers
            Path("/path/to/foo-1"),
            Path("/path/to/foo-2"),
            Path("/path/to/foo-1.md"),
            Path("/path/to/foo-2.md"),
            Path("/path/to/foo-3.md"),
            Path("/path/to/foo-1.txt"),
            Path("/path/to/foo-2.txt"),
            Path("/path/to/foo-3.txt"),
            Path("/path/to/foo-4.txt"),
            Path("/path/to/foo-1.txt.tar.gz"),
            Path("/path/to/foo-2.txt.tar.gz"),
        ],
    )


class TestSiblings:
    def test_should_return_generator_of_numbered_files(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        siblings = file.siblings
        assert isinstance(siblings, types.GeneratorType)
        assert isinstance(next(siblings), NumberedFile)

    def test_should_be_empty_when_no_parent_dir(self, fake_files):
        file = NumberedFile.of("/no/such/path")
        assert list(file.siblings) == []

    def test_should_be_empty_when_no_such_file(self, fake_files):
        file = NumberedFile.of("/path/to/no-such-file")
        assert list(file.siblings) == []

    def test_should_retain_parent(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        sibling = next(file.siblings)
        assert sibling.parent == Path("/path/to")

    @pytest.mark.parametrize(
        "path, expected_siblings",
        [
            (
                "/path/to/foo",
                {
                    Path("/path/to/foo"),
                    Path("/path/to/foo-1"),
                    Path("/path/to/foo-2"),
                },
            ),
            (
                "/path/to/foo.txt",
                {
                    Path("/path/to/foo.txt"),
                    Path("/path/to/foo-1.txt"),
                    Path("/path/to/foo-2.txt"),
                    Path("/path/to/foo-3.txt"),
                    Path("/path/to/foo-4.txt"),
                },
            ),
            (
                "/path/to/foo.txt.tar.gz",
                {
                    Path("/path/to/foo.txt.tar.gz"),
                    Path("/path/to/foo-1.txt.tar.gz"),
                    Path("/path/to/foo-2.txt.tar.gz"),
                },
            ),
            (
                "/path/to/foo.md",
                {
                    Path("/path/to/foo.md"),
                    Path("/path/to/foo-1.md"),
                    Path("/path/to/foo-2.md"),
                    Path("/path/to/foo-3.md"),
                },
            ),
            (
                "/path/to/foobar",
                {
                    Path("/path/to/foobar"),
                },
            ),
            (
                "/path/to/foobar.md",
                {
                    Path("/path/to/foobar.md"),
                },
            ),
            (
                "/path/to/foobar.txt",
                {
                    Path("/path/to/foobar.txt"),
                },
            ),
            (
                "/path/to/foobar.txt.tar.gz",
                {
                    Path("/path/to/foobar.txt.tar.gz"),
                },
            ),
            (
                "/path/to/file",
                {
                    Path("/path/to/file-1"),
                    Path("/path/to/file-2"),
                    Path("/path/to/file-3"),
                    Path("/path/to/file-4"),
                },
            ),
            (
                "/path/to/lorem",
                {
                    Path("/path/to/lorem"),
                    Path("/path/to/lorem-2"),
                    Path("/path/to/lorem-3"),
                },
            ),
            (
                "/path/to/ipsum",
                {
                    Path("/path/to/ipsum-3"),
                    Path("/path/to/ipsum-8"),
                    Path("/path/to/ipsum-9"),
                    Path("/path/to/ipsum-12"),
                },
            ),
            (
                "/path/to/main.py",
                {
                    Path("/path/to/main.py"),
                },
            ),
        ],
    )
    def test_should_filter_files_by_name_and_suffix(
        self, path, expected_siblings, fake_files
    ):
        file = NumberedFile.of(path)
        siblings = set(sibling.path for sibling in file.siblings)
        assert siblings == expected_siblings

    @pytest.mark.parametrize(
        "path, expected_siblings",
        [
            (
                "/path/to/foo-42",
                {
                    Path("/path/to/foo"),
                    Path("/path/to/foo-1"),
                    Path("/path/to/foo-2"),
                },
            ),
            (
                "/path/to/foo-42.txt",
                {
                    Path("/path/to/foo.txt"),
                    Path("/path/to/foo-1.txt"),
                    Path("/path/to/foo-2.txt"),
                    Path("/path/to/foo-3.txt"),
                    Path("/path/to/foo-4.txt"),
                },
            ),
            (
                "/path/to/foo-42.txt.tar.gz",
                {
                    Path("/path/to/foo.txt.tar.gz"),
                    Path("/path/to/foo-1.txt.tar.gz"),
                    Path("/path/to/foo-2.txt.tar.gz"),
                },
            ),
        ],
    )
    def test_should_ignore_given_number(
        self, path, expected_siblings, fake_files
    ):
        file = NumberedFile.of(path)
        siblings = set(sibling.path for sibling in file.siblings)
        assert siblings == expected_siblings


class TestSiblingsAscending:
    def test_should_return_list_of_numbered_files(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        siblings_ascending = file.siblings_ascending
        assert isinstance(siblings_ascending, list)
        assert isinstance(siblings_ascending[0], NumberedFile)

    def test_should_be_empty_when_no_parent_dir(self, fake_files):
        file = NumberedFile.of("/no/such/path")
        assert file.siblings_ascending == []

    def test_should_be_empty_when_no_such_file(self, fake_files):
        file = NumberedFile.of("/path/to/no-such-file")
        assert file.siblings_ascending == []

    @pytest.mark.parametrize(
        "path, expected_siblings",
        [
            (
                "/path/to/foo",
                [
                    Path("/path/to/foo"),
                    Path("/path/to/foo-1"),
                    Path("/path/to/foo-2"),
                ],
            ),
            (
                "/path/to/ipsum",
                [
                    Path("/path/to/ipsum-3"),
                    Path("/path/to/ipsum-8"),
                    Path("/path/to/ipsum-9"),
                    Path("/path/to/ipsum-12"),
                ],
            ),
        ],
    )
    def test_should_have_increasing_number(
        self, path: str, expected_siblings: list, fake_files
    ):
        file = NumberedFile.of(path)
        siblings_ascending = [
            sibling.path for sibling in file.siblings_ascending
        ]
        assert siblings_ascending == expected_siblings


class TestSiblingsDescending:
    def test_should_return_list_of_numbered_files(self, fake_files):
        file = NumberedFile.of("/path/to/file")
        siblings_descending = file.siblings_descending
        assert isinstance(siblings_descending, list)
        assert isinstance(siblings_descending[0], NumberedFile)

    def test_should_be_empty_when_no_parent_dir(self, fake_files):
        file = NumberedFile.of("/no/such/path")
        assert file.siblings_descending == []

    def test_should_be_empty_when_no_such_file(self, fake_files):
        file = NumberedFile.of("/path/to/no-such-file")
        assert file.siblings_descending == []

    @pytest.mark.parametrize(
        "path, expected_siblings",
        [
            (
                "/path/to/foo",
                [
                    Path("/path/to/foo-2"),
                    Path("/path/to/foo-1"),
                    Path("/path/to/foo"),
                ],
            ),
            (
                "/path/to/ipsum",
                [
                    Path("/path/to/ipsum-12"),
                    Path("/path/to/ipsum-9"),
                    Path("/path/to/ipsum-8"),
                    Path("/path/to/ipsum-3"),
                ],
            ),
        ],
    )
    def test_should_have_decreasing_number(
        self, path: str, expected_siblings: list, fake_files
    ):
        file = NumberedFile.of(path)
        siblings_descending = [
            sibling.path for sibling in file.siblings_descending
        ]
        assert siblings_descending == expected_siblings


class TestOpenAll:
    def test_should_open_ascending_siblings(
        self, mocker: MockerFixture, fake_files
    ):

        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)

        expected_calls = [
            call(Path("/path/to/foo.txt"), mode="r", encoding="utf-8"),
            call(Path("/path/to/foo-1.txt"), mode="r", encoding="utf-8"),
            call(Path("/path/to/foo-2.txt"), mode="r", encoding="utf-8"),
            call(Path("/path/to/foo-3.txt"), mode="r", encoding="utf-8"),
            call(Path("/path/to/foo-4.txt"), mode="r", encoding="utf-8"),
        ]

        for i, file in enumerate(open_all("/path/to/foo.txt", mode="r")):
            assert expected_calls[i] == mock_open.call_args

    def test_should_close_all_files_automatically(
        self, mocker: MockerFixture, fake_files
    ):
        mocker.patch("builtins.open", mocker.mock_open(read_data="fake data"))
        files = []
        for file in open_all("/path/to/foo.txt", mode="r"):
            assert file.read() == "fake data"
            files.append(file)
        for file in files:
            file.close.assert_called()

    def test_should_open_in_read_mode_by_default(
        self, mocker: MockerFixture, fake_files
    ):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        for _ in enumerate(open_all("/path/to/foo.txt")):
            assert mock_open.call_args.kwargs["mode"] == "r"


class TestOpenLatest:
    def test_read_no_such_file(self, mocker: MockerFixture, fake_files):
        mocker.patch.object(Path, "exists", side_effect=[False])
        with pytest.raises(FileNotFoundError):
            open_latest("/path/to/no-such-file", mode="r")

    def test_write_no_such_file(self, mocker: MockerFixture, fake_files):
        mocker.patch("builtins.open", mocker.mock_open())
        mocker.patch.object(Path, "exists", side_effect=[False])
        open_latest("/path/to/no-such-file", mode="w")

    def test_read_existing_file(self, mocker: MockerFixture, fake_files):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mocker.patch.object(Path, "exists", side_effect=[True])
        open_latest("/path/to/file", mode="r")
        mock_open.assert_called_once_with(
            Path("/path/to/file-4"), mode="r", encoding="utf-8"
        )

    def test_write_existing_file(self, mocker: MockerFixture, fake_files):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mocker.patch.object(Path, "exists", side_effect=[True])
        open_latest("/path/to/file", mode="w")
        mock_open.assert_called_once_with(
            Path("/path/to/file-4"), mode="w", encoding="utf-8"
        )

    def test_should_open_in_append_mode_by_default(
        self, mocker: MockerFixture, fake_files
    ):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        for _ in enumerate(open_latest("/path/to/foo.txt")):
            assert mock_open.call_args.kwargs["mode"] == "a"


class TestOpenNext:
    def test_read_no_such_file(self, mocker: MockerFixture, fake_files):
        mocker.patch.object(Path, "exists", return_value=False)
        with pytest.raises(FileNotFoundError):
            open_next("/path/to/no-such-file", mode="r")

    def test_write_no_such_file(self, mocker: MockerFixture, fake_files):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mocker.patch.object(Path, "exists", return_value=False)
        open_next("/path/to/no-such-file", mode="w")
        mock_open.assert_called_once_with(
            Path("/path/to/no-such-file-1"), mode="w", encoding="utf-8"
        )

    def test_read_existing_file(self, mocker: MockerFixture, fake_files):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mocker.patch.object(Path, "exists", return_value=True)
        open_next("/path/to/file", mode="r")
        mock_open.assert_called_once_with(
            Path("/path/to/file-5"), mode="r", encoding="utf-8"
        )

    def test_write_existing_file(self, mocker: MockerFixture, fake_files):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        mocker.patch.object(Path, "exists", return_value=True)
        open_next("/path/to/file", mode="w")
        mock_open.assert_called_once_with(
            Path("/path/to/file-5"), mode="w", encoding="utf-8"
        )

    def test_should_open_in_write_mode_by_default(
        self, mocker: MockerFixture, fake_files
    ):
        mock_open = mocker.mock_open()
        mocker.patch("builtins.open", mock_open)
        for _ in enumerate(open_next("/path/to/foo.txt")):
            assert mock_open.call_args.kwargs["mode"] == "w"
