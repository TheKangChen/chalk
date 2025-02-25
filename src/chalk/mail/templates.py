from email.message import EmailMessage
from pathlib import Path
from string import Template
from typing import Dict, Any
from dataclasses import dataclass
import json


@dataclass
class EmailTemplate:
    """Represents an email template with HTML and plain text versions"""

    html_content: str
    plain_content: str
    default_variables: Dict[str, Any]

    @classmethod
    def from_files(
        cls, html_path: Path, plain_path: Path, variables_path: Path
    ) -> "EmailTemplate":
        """Load template from files. Plain text is optional."""
        if not plain_path.exists():
            raise FileNotFoundError(f"Plain text template not found: {plain_path}")
        if not variables_path.exists():
            raise FileNotFoundError(f"Variables file not found: {variables_path}")

        html_content = html_path.read_text(encoding="utf-8")
        plain_content = plain_path.read_text(encoding="utf-8")
        default_variables = json.loads(variables_path.read_text(encoding="utf-8"))

        return cls(
            html_content=html_content,
            plain_content=plain_content,
            default_variables=default_variables,
        )


# TODO: Replace string template directory with config
class EmailTemplateEngine:
    """Manages email templates and creates EmailMessage objects"""

    def __init__(self, template_dir: str = "../config/email_templates"):
        self.template_dir = Path(template_dir)
        self.templates: Dict[str, EmailTemplate] = {}
        self.load_templates()

    def load_templates(self):
        """Load all template pairs from the template directory"""
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory {self.template_dir} not found")

        # Load each HTML template and its corresponding plain text version if it exists
        for html_file in self.template_dir.glob("*.html"):
            template_name = html_file.stem
            plain_file = html_file.with_suffix(".txt")

            self.templates[template_name] = EmailTemplate.from_files(
                html_file, plain_file if plain_file.exists() else None
            )

    def create_email(
        self,
        template_name: str,
        custom_variables: Dict[str, Any],
        bcc: list[str] = None,
    ) -> EmailMessage:
        """
        Create an email using template and variables

        Args:
            template_name: Name of the template to use
            custom_variables: Variables to override defaults
            bcc: Optional list of BCC recipients

        Returns:
            EmailMessage object with HTML and plain text content
        """
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")

        template = self.templates[template_name]

        # Merge default variables with custom ones
        variables = template.default_variables.copy()
        variables.update(custom_variables)

        # Create Template objects for substitution
        html_template = Template(template.html_content)
        plain_template = Template(template.plain_content)

        # Create email message
        message = EmailMessage()
        message["Subject"] = variables.get("subject", "").format(**custom_variables)
        message["From"] = variables.get("from_email")
        message["To"] = variables.get("to_email")
        message["Cc"] = variables.get("cc")

        if bcc:
            message["Bcc"] = ", ".join(bcc)

        # Set content with variable substitution
        try:
            message.set_content(plain_template.substitute(variables))
            message.add_alternative(html_template.substitute(variables), subtype="html")
        except KeyError as e:
            raise ValueError(f"Missing required variable: {e}")

        return message


if __name__ == "__main__":
    engine = EmailTemplateEngine()
    message = engine.create_email(
        template_name="example_template",
        custom_variables={
            "date": "January 29, 2024",
            "start_time": "2:00 PM",
        },
        bcc=["student1@email.com", "student2@email.com"],
    )
