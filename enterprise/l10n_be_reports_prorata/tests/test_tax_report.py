from odoo import fields
from odoo.addons.account_reports.tests.account_sales_report_common import AccountSalesReportCommon
from odoo.tests import tagged
from freezegun import freeze_time


@tagged('post_install_l10n', 'post_install', '-at_install')
class TestBelgiumTaxReportProrata(AccountSalesReportCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref='l10n_be.l10nbe_chart_template'):
        super().setUpClass(chart_template_ref)

    @classmethod
    def setup_company_data(cls, company_name, chart_template=None, **kwargs):
        res = super().setup_company_data(company_name, chart_template=chart_template, **kwargs)
        res['company'].update({
            'country_id': cls.env.ref('base.be').id,
            'vat': 'BE0477472701',
        })
        res['company'].partner_id.update({
            'email': 'jsmith@mail.com',
            'phone': '+32475123456',
        })
        return res

    @freeze_time('2019-04-15')
    def test_generate_xml_with_prorata(self):
        company = self.env.company
        report = self.env['account.generic.tax.report']
        options = report._get_options(None)

        wizard_action = report.l10n_be_print_xml(options)
        wizard = self.env[wizard_action['res_model']].with_context(wizard_action['context']).browse(wizard_action['res_id'])
        wizard.write({
            'is_prorata_necessary': True,
            'prorata_year': 2019,
            'prorata': 25,
            'prorata_at_100': 50,
            'prorata_at_0': 50,
        })

        wizard.print_xml()

        # The partner id is changing between execution of the test so we need to append it manually to the reference.
        # Declaring March month, so 3
        ref = str(company.partner_id.id) + '032019'

        # This is the minimum expected from the belgian tax report xml.
        # As no values are in the report, we only find the grid 71 which is always expected to be present.
        expected_xml = """
        <ns2:VATConsignment xmlns="http://www.minfin.fgov.be/InputCommon" xmlns:ns2="http://www.minfin.fgov.be/VATConsignment" VATDeclarationsNbr="1">
            <ns2:VATDeclaration SequenceNumber="1" DeclarantReference="%s">
                <ns2:Declarant>
                    <VATNumber xmlns="http://www.minfin.fgov.be/InputCommon">0477472701</VATNumber>
                    <Name>company_1_data</Name>
                    <Street></Street>
                    <PostCode></PostCode>
                    <City></City>
                    <CountryCode>BE</CountryCode>
                    <EmailAddress>jsmith@mail.com</EmailAddress>
                    <Phone>+32475123456</Phone>
                </ns2:Declarant>
                <ns2:Period>
                    <ns2:Month>03</ns2:Month>
                    <ns2:Year>2019</ns2:Year>
                </ns2:Period>
                <ns2:Deduction>
                    <AdjustedPeriod>2019</AdjustedPeriod>
                    <AdjustedValue>25</AdjustedValue>
                    <SpecialAdjustedValue>
                        <UseProRataPercentage GridNumber="1">50</UseProRataPercentage>
                        <UseProRataPercentage GridNumber="2">50</UseProRataPercentage>
                        <UseProRataPercentage GridNumber="3">0</UseProRataPercentage>
                    </SpecialAdjustedValue>
                </ns2:Deduction>
                <ns2:Data>
                    <ns2:Amount GridNumber="71">0.00</ns2:Amount>
                </ns2:Data>
                <ns2:ClientListingNihil>NO</ns2:ClientListingNihil>
                <ns2:Ask Restitution="NO" Payment="NO"/>
                <ns2:Comment></ns2:Comment>
            </ns2:VATDeclaration>
        </ns2:VATConsignment>
        """ % ref

        self.assertXmlTreeEqual(
            self.get_xml_tree_from_string(report.get_xml(options)),
            self.get_xml_tree_from_string(expected_xml)
        )