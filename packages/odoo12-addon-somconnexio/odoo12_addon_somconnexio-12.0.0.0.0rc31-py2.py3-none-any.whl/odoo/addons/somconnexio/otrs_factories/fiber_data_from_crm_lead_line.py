from otrs_somconnexio.otrs_models.fiber_data import FiberData


class FiberDataFromCRMLeadLine:

    def __init__(self, crm_lead_line):
        self.crm_lead_line = crm_lead_line

    def build(self):
        isp_info = self.crm_lead_line.broadband_isp_info

        return FiberData(
            order_id=self.crm_lead_line.id,
            phone_number=isp_info.phone_number,
            service_address=isp_info.service_full_street,
            service_city=isp_info.service_city,
            service_zip=isp_info.service_zip_code,
            service_subdivision=isp_info.service_state_id.name,
            shipment_address=isp_info.delivery_full_street,
            shipment_city=isp_info.delivery_city,
            shipment_zip=isp_info.delivery_zip_code,
            shipment_subdivision=isp_info.delivery_state_id.name,
            previous_provider=isp_info.previous_provider.name or 'None',
            previous_owner_vat=isp_info.previous_owner_vat_number or '',
            previous_owner_name=isp_info.previous_owner_first_name or '',
            previous_owner_surname=isp_info.previous_owner_name or '',
            previous_service=isp_info.previous_service,
            notes=self.crm_lead_line.lead_id.description,
            iban=self.crm_lead_line.lead_id.iban,
            product=self.crm_lead_line.product_id.default_code,
            adsl_coverage=isp_info.adsl_coverage,
            mm_fiber_coverage=isp_info.mm_fiber_coverage,
            vdf_fiber_coverage=isp_info.vdf_fiber_coverage,
            change_address='yes' if isp_info.change_address else 'no',
            previous_internal_provider=isp_info.service_supplier_id,
        )
