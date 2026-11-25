import pytest

from sanitise import sanitise


@pytest.mark.parametrize(
    ("name", "text", "sensitive_value"),
    [
        ("INDIAN_MOBILE", "Call +91 9876543210", "+91 9876543210"),
        ("INDIAN_MOBILE", "Call 9876543210", "9876543210"),
        ("INDIAN_MOBILE", "Call +91-98765 43210", "+91-98765 43210"),
        ("EMPLOYEE_ID", "Owner HM-123456", "HM-123456"),
        ("AWS_ACCESS_KEY", "Key AKIA1234567890ABCDEF", "AKIA1234567890ABCDEF"),
        (
            "AWS_SECRET",
            "aws_secret_access_key=abcdefghijklmnopqrstuvwxyz1234567890ABCD",
            "abcdefghijklmnopqrstuvwxyz1234567890ABCD",
        ),
        ("AWS_SECRET", "key and secret " + "A" * 40, "A" * 40),
        ("BEARER_TOKEN", "Authorization: Bearer abc.def-123", "Bearer abc.def-123"),
        (
            "BEARER_TOKEN",
            "JWT eyJhbGci.eyJzdWI.signature",
            "eyJhbGci.eyJzdWI.signature",
        ),
        (
            "UNC_PATH",
            r"File at \\server\shared folder\folder\file.txt",
            r"\\server\shared folder\folder\file.txt",
        ),
        (
            "CONNECTION_STRING_PASSWORD",
            "Server=db;Password='two words';User ID=admin",
            "Password='two words'",
        ),
    ],
)
def test_sanitise_masks_named_patterns(name, text, sensitive_value):
    cleaned, found = sanitise(text, {})

    assert name in found
    assert sensitive_value not in cleaned
    assert f"<{name}_1>" in cleaned


def test_mobile_pattern_does_not_match_digits_inside_longer_number():
    cleaned, found = sanitise("Reference 198765432101", {})

    assert "INDIAN_MOBILE" not in found
    assert cleaned == "Reference 198765432101"
