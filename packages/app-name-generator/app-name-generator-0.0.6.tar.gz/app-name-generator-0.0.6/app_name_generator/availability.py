import dns.resolver


def domain_fully_available(domain_name, exclusive=False, tlds=["com", "fr", "io"]):
    domains = []
    for tld in tlds:
        fqdn = domain_name + "." + tld
        try:
            dns.resolver.resolve(fqdn)
            if exclusive:
                return []
        except (
            dns.exception.Timeout,
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
        ):
            domains.append(fqdn)
        except dns.name.EmptyLabel:
            pass
    return domains
