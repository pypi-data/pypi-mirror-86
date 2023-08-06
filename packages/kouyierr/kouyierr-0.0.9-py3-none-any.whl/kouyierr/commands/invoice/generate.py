''' Invoice generator module.

    Parameters:
        year (int): Year of the invoice, default=current
        month (int): Month of the invoice, default=current
        company_config (str): Company config file
        invoice_config (str): Invoice config file
        template (str): Template file path
'''
import calendar
import datetime
import logging
import os
import time
import click
from jinja2 import Environment, FileSystemLoader, TemplateError
import pdfkit
from rich import print as rprint
from rich.console import Console
import yaml

from kouyierr.commands import global_options
from kouyierr.utils.helper import Helper


class Generator:
    ''' Invoice generator class '''
    def __init__(self, helper: Helper, year: int, month: int, company_config: str, invoice_config: str, template: str):
        logging.basicConfig(format='%(message)s')
        logging.getLogger(__package__).setLevel(logging.INFO)
        self._logger = logging.getLogger(__name__)
        self._helper = helper
        self._year = year
        self._month = month
        self._company_config = company_config
        self._invoice_config = invoice_config
        self._template = template

    def load_config(self, year: int, month: int, company_config: str, invoice_config: str) -> dict():
        ''' Build dict config based on local YAML files '''
        try:
            global_config = yaml.load(open(company_config), Loader=yaml.FullLoader)
            invoice_config = yaml.load(open(invoice_config), Loader=yaml.FullLoader)
            config = {**global_config, **invoice_config} # merge both dict()
        except TypeError as exception:
            self._logger.error("Error loading invoice file: %s", exception)
            raise
        # static tax compute (to avoid Jinja2 complex filter use)
        config['invoice_total_ht'] = 0
        for invoice_item in invoice_config['invoice_items']:
            config['invoice_total_ht'] += (invoice_item['quantity'] * invoice_item['unit_price'])
        # static items generation, yes we're lazy
        config['title'] = f"{config['customer_name']} | {year}{month}"
        config['invoice_id'] = f"{year}{month}_{config['customer_id']}"
        # retrieve last day of month, aka golden day
        config['generated_date'] = f'{calendar.monthrange(year, month)[1]}/{month}/{year}'
        invoice_due_date = datetime.datetime.strptime(config['generated_date'], '%d/%m/%Y') \
            + datetime.timedelta(days=30)
        config['invoice_due_date'] = f'{invoice_due_date.day}/{invoice_due_date.month}/{invoice_due_date.year}'
        return config

    def load_template(self, template: str):
        ''' Load Jinja2 template and attach a custom filter for currency format '''
        try:
            template_file = os.path.basename(template)
            template_path = os.path.dirname(template)
            env = Environment(loader=FileSystemLoader(template_path))
            env.filters['format_currency'] = self._helper.format_currency
            return env.get_template(template_file)
        except TemplateError as exception:
            self._logger.error(exception)
            raise

    def execute(self):
        start_time = time.time()
        rprint("[bold green]Starting invoice generation[/bold green] lucky :bear: ...")
        config = self.load_config(
            year=self._year,
            month=self._month,
            company_config=os.path.abspath(self._company_config),
            invoice_config=os.path.abspath(self._invoice_config)
        )
        rprint("[bold yellow]Following configuration has been loaded:[/bold yellow]")
        console = Console()
        console.log(config)
        template = self.load_template(os.path.abspath(self._template))
        output_from_parsed_template = template.render(config)
        html_file_path = os.path.join(os.getcwd(), f"{self._year}{self._month}_{config['customer_id']}.html")
        pdf_file_path = os.path.join(os.getcwd(), f"{self._year}{self._month}_{config['customer_id']}.pdf")
        pdfkit_options = {'quiet': ''}
        with open(html_file_path, "w") as file_stream:
            file_stream.write(output_from_parsed_template)
            rprint(f"[blue]HTML file {html_file_path} has been generated![/blue]")
        pdfkit.from_string(
            input=output_from_parsed_template,
            output_path=pdf_file_path,
            options=pdfkit_options
        )
        rprint(f"[blue]PDF file {pdf_file_path} has been generated![/blue]")
        elapsed_time = round(time.time() - start_time, 2)
        rprint(f"[bold green]Invoice generation complete[/bold green] in {elapsed_time}s :thumbs_up:")


@click.command(help='Generate a new invoice based on definition file and company template')
@global_options
@click.option('--year', required=False, type=int, default=datetime.datetime.now().year,
              help='Year of the invoice, default=current')
@click.option('--month', required=False, type=int, default=datetime.datetime.now().month,
              help='Month of the invoice, default=current')
@click.option('--company_config', required=True, type=str, help='Company config file')
@click.option('--invoice_config', required=True, type=str, help='Invoice config file')
@click.option('--template', required=True, type=str, help='Template file path')
def generate(year: int, month: int, company_config: str, invoice_config: str, template: str):
    ''' Generate a new invoice based on definition file and company template '''
    Generator(Helper(), year, month, company_config, invoice_config, template).execute()
