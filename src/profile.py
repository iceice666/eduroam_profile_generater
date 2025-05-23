"""
Profile generation module for the eduroam profile generator.
"""

from typing import Optional

from src.constants import (
    TEMPLATE_DIR,
    PROFILE_DIR,
    GETEDUROAM_TEMPLATE_BOTH,
    GETEDUROAM_TEMPLATE_PEAP_MSCHAPV2,
    GETEDUROAM_TEMPLATE_TTLS_PAP,
)


def generate_profile(
    realm: str,
    name: str,
    short_name: str,
    mschapv2_stat: bool,
    pap_stat: bool,
    dns: str,
    url: str,
    mschapv2_cert: str,
    pap_cert: str,
) -> Optional[str]:
    """
    Generate eduroam profile configuration file.

    Args:
        realm: Domain realm
        name: Profile name
        short_name: Short name for the profile
        mschapv2_stat: MSCHAPv2 authentication status
        pap_stat: PAP authentication status
        dns: DNS server
        url: URL for more information
        mschapv2_cert: MSCHAPv2 certificate
        pap_cert: PAP certificate

    Returns:
        Generated profile filename or None if failed
    """
    # Select appropriate template based on authentication methods
    if mschapv2_stat and pap_stat:
        source_file = GETEDUROAM_TEMPLATE_BOTH
    elif pap_stat:
        source_file = GETEDUROAM_TEMPLATE_TTLS_PAP
    elif mschapv2_stat:
        source_file = GETEDUROAM_TEMPLATE_PEAP_MSCHAPV2
    else:
        print("未知的錯誤")
        return None

    print()
    print(source_file, "\n成功複製到編輯暫存目錄！")

    # Read template file
    template_path = TEMPLATE_DIR / source_file
    with open(template_path, "r", encoding="utf-8") as file:
        config_content = file.read()

    # Replace template variables
    replacements = {
        "#Realm#": realm,
        "#PEAP_MSCHAPv2Cert#": mschapv2_cert,
        "#TTLS_PAPCert#": pap_cert,
        "#Domain#": dns,
        "#Name#": f"{name} Compatible Profile",
        "#Desc#": f"Profile generated by third party, suitable for accounts with @{realm}",
        "#Email#": "eduroamtw@googlegroups.com",
        "#URL#": url,
        "#Tel#": "NULL",
    }

    for placeholder, value in replacements.items():
        config_content = config_content.replace(placeholder, value)

    # Write profile file
    profile_filename = f"eduroam-eap-generic-{short_name}.eap-config"
    profile_path = PROFILE_DIR / profile_filename

    with open(profile_path, "w", encoding="utf-8") as file:
        file.write(config_content)

    return profile_filename
