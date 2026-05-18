# OCI Marketplace / OCI Generative AI Checklist

Steps to subscribe and verify billing via your OCI credits:

1. Sign in to the Oracle Cloud Console and confirm available credits on the Billing page.
2. Open **Oracle Cloud Marketplace** (Marketplace → OCI listings) and search for "Generative AI" or the model vendor.
3. On a listing page, confirm the **Pricing & Billing** section — offerings that bill to your OCI account will state billing via OCI/Marketplace.
4. Subscribe/launch the offering from the Marketplace; confirm that the billing is to your tenancy (compartment).
5. Test the service per the provider instructions. If the provider exposes an endpoint, use their example request to validate functionality.

Compute fallback (self‑host using credits): example `oci` CLI command to launch a GPU instance (replace placeholders):

```bash
oci compute instance launch \
  --availability-domain '<AD>' \
  --compartment-id '<COMPARTMENT_OCID>' \
  --shape 'VM.GPU.A10.1' \
  --display-name 'ai-bible-gpu' \
  --image-id '<IMAGE_OCID_FOR_UBUNTU_22_04>' \
  --subnet-id '<SUBNET_OCID>' \
  --assign-public-ip true \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
  --boot-volume-size-in-gbs 100
```

If you want, I can: (A) check your tenancy for Marketplace offers, or (B) generate a `docker-compose` that launches both `vLLM` and `translator` services and pulls a quantized model automatically.
