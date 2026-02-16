"""
HTML email template renderer.

Renders an EmailDigest into a responsive HTML email suitable for
delivery via SES. Uses inline CSS and table-based layout for
email client compatibility.

The template includes a {{unsubscribe_url}} placeholder that the
Lambda email sender replaces per-subscriber.
"""

from .agents.email_digest import EmailDigest


def render_email_html(
    digest: EmailDigest,
    brief_date: str,
    brief_url: str,
) -> str:
    """
    Render an EmailDigest into an HTML email string.

    Args:
        digest: The condensed email digest
        brief_date: Display date for the brief (e.g., "February 8, 2026")
        brief_url: URL to the full brief on the web

    Returns:
        Complete HTML email string with {{unsubscribe_url}} placeholder
    """
    # Build region sections
    region_blocks = []
    for region in digest.regions:
        region_blocks.append(
            _REGION_BLOCK.format(
                region_name=_escape(region.name),
                region_summary=_escape(region.summary),
            )
        )
    regions_html = "\n".join(region_blocks)

    return _TEMPLATE.format(
        brief_date=_escape(brief_date),
        lede=_escape(digest.lede),
        regions=regions_html,
        brief_url=_escape(brief_url),
    )


def _escape(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# Font stacks — Atkinson Hyperlegible Next matching the web version,
# with safe fallbacks for email clients that strip <link> tags.
_FONT = "'Atkinson Hyperlegible Next',Helvetica,Arial,sans-serif"

_REGION_BLOCK = (
    '                        <tr>\n'
    '                          <td style="padding:0 0 20px 0;">\n'
    '                            <h2 style="margin:0 0 8px 0;font-size:16px;'
    'font-weight:700;color:#1a1a2e;font-family:FONT_STACK;">{region_name}</h2>\n'
    '                            <p style="margin:0;font-size:15px;line-height:1.55;'
    'color:#333333;font-family:FONT_STACK;">{region_summary}</p>\n'
    '                          </td>\n'
    '                        </tr>'
).replace("FONT_STACK", _FONT)

_TEMPLATE = ("""\
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>The Middle Powers Monitor &mdash; {brief_date}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,700;1,400;1,700&display=swap">
  <!--[if mso]>
  <noscript>
    <xml>
      <o:OfficeDocumentSettings>
        <o:PixelsPerInch>96</o:PixelsPerInch>
      </o:OfficeDocumentSettings>
    </xml>
  </noscript>
  <![endif]-->
  <style>
    body,table,td,a{{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;}}
    table,td{{mso-table-lspace:0pt;mso-table-rspace:0pt;}}
    img{{-ms-interpolation-mode:bicubic;border:0;height:auto;line-height:100%;outline:none;text-decoration:none;}}
    body{{margin:0;padding:0;width:100%!important;background-color:#f4f4f7;}}
    @media only screen and (max-width:620px) {{
      .email-container {{width:100%!important;}}
      .stack-column {{display:block!important;width:100%!important;}}
    }}
  </style>
</head>
<body style="margin:0;padding:0;background-color:#f4f4f7;">
  <center style="width:100%;background-color:#f4f4f7;">
    <!--[if mso]>
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center"><tr><td>
    <![endif]-->
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width:600px;margin:0 auto;" class="email-container">

      <!-- HEADER -->
      <tr>
        <td style="padding:24px 24px 16px 24px;background-color:#1a1a2e;">
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
            <tr>
              <td style="font-family:FONT_STACK;font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#8888aa;">THE MIDDLE POWERS MONITOR</td>
            </tr>
            <tr>
              <td style="padding-top:4px;font-family:FONT_STACK;font-size:22px;font-weight:700;color:#ffffff;">{brief_date}</td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- LEDE -->
      <tr>
        <td style="padding:28px 24px 24px 24px;background-color:#ffffff;">
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
            <tr>
              <td style="font-family:FONT_STACK;font-size:11px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;color:#888888;padding-bottom:10px;">THIS WEEK</td>
            </tr>
            <tr>
              <td style="font-family:FONT_STACK;font-size:16px;line-height:1.6;color:#1a1a2e;">{lede}</td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- DIVIDER -->
      <tr>
        <td style="padding:0 24px;background-color:#ffffff;">
          <hr style="border:none;border-top:1px solid #e0e0e0;margin:0;">
        </td>
      </tr>

      <!-- REGIONS -->
      <tr>
        <td style="padding:24px;background-color:#ffffff;">
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
{regions}
          </table>
        </td>
      </tr>

      <!-- CTA BUTTON -->
      <tr>
        <td style="padding:0 24px 32px 24px;background-color:#ffffff;">
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
            <tr>
              <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td style="border-radius:6px;background-color:#1a1a2e;">
                      <a href="{brief_url}" target="_blank" style="display:inline-block;padding:14px 32px;font-family:FONT_STACK;font-size:14px;font-weight:600;color:#ffffff;text-decoration:none;border-radius:6px;">Read the full brief &rarr;</a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- FOOTER -->
      <tr>
        <td style="padding:20px 24px;background-color:#f4f4f7;">
          <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
            <tr>
              <td style="font-family:FONT_STACK;font-size:12px;line-height:1.5;color:#999999;text-align:center;">
                The Middle Powers Monitor &mdash; Weekly geopolitical intelligence<br>
                <a href="{{{{unsubscribe_url}}}}" style="color:#999999;text-decoration:underline;">Unsubscribe</a>
              </td>
            </tr>
          </table>
        </td>
      </tr>

    </table>
    <!--[if mso]>
    </td></tr></table>
    <![endif]-->
  </center>
</body>
</html>""").replace("FONT_STACK", _FONT)
