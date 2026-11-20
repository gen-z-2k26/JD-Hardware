import { CONTENT_PAGES } from "@/lib/site-urls";
import type { FaqGroup } from "@/lib/types";

export type PolicySection = {
  title: string;
  paragraphs?: string[];
  bullets?: string[];
};

export type PolicyPageDef = {
  slug: string;
  title: string;
  description: string;
  intro: string;
  groupTitles: string[];
  paragraphs?: string[];
  designed?: boolean;
  sections?: PolicySection[];
};

export const POLICY_PAGES: PolicyPageDef[] = [
  {
    slug: "shipping-policy",
    title: "Shipping & Delivery",
    description:
      "At JD Hardware, operated by JD Hardware Co., we aim to provide clear information about shipping costs, order processing and delivery throughout the United Kingdom.",
    intro:
      "Standard UK shipping is free. Published estimates are 1-2 business days handling and 3-5 business days in transit.",
    groupTitles: ["Shipping and Delivery"],
  },
  {
    slug: "return-and-refund-policy",
    title: "Returns & Refunds",
    description:
      "At JD Hardware, we aim to make returning eligible products straightforward and transparent.",
    intro:
      "Eligible products may be returned within 28 days. Approved returns include a JD Hardware return label, £0.00 return shipping, and a £0.00 restocking fee.",
    groupTitles: ["Returns and Refunds"],
  },
  {
    slug: "cancellation-policy",
    title: "Order Cancellations",
    description: "We understand that customers may need to cancel an order.",
    intro:
      "Contact us as soon as possible if you wish to cancel. Your statutory cancellation rights may apply even after an order has entered fulfilment.",
    groupTitles: ["Orders and Payments"],
  },
  {
    slug: "payment-policy",
    title: "Payment Options",
    description:
      "JD Hardware aims to provide a clear and convenient online checkout experience.",
    intro:
      "The payment methods currently accepted by JD Hardware are displayed during checkout. Prices and transactions are in pounds sterling (GBP).",
    groupTitles: ["Orders and Payments"],
  },
  {
    slug: "buy-now-pay-later",
    title: "Buy Now, Pay Later",
    description:
      "The payment methods currently accepted by JD Hardware are displayed during checkout.",
    intro:
      "The payment methods currently accepted by JD Hardware are displayed during checkout. We do not guarantee acceptance of a particular payment method unless it is shown as available at checkout.",
    groupTitles: [],
  },
  {
    slug: "warranty",
    title: "Warranty & Support",
    description:
      "JD Hardware provides assistance with product enquiries, damaged deliveries, defects and applicable warranty information.",
    intro:
      "Warranty coverage may vary depending on the product and manufacturer. Statutory rights relating to faulty goods still apply.",
    groupTitles: ["Products and Warranty"],
  },
  {
    slug: "privacy-policy",
    title: "Privacy Policy",
    description:
      "At JD Hardware, operated by JD Hardware Co., we respect the privacy of customers and website visitors.",
    intro:
      "This Privacy Policy explains how we may collect, use, store and disclose personal information when you visit https://jdhardware.shop or purchase products from us.",
    groupTitles: [],
  },
  {
    slug: "terms-of-service",
    title: "Terms & Conditions",
    description:
      "These Terms & Conditions govern purchases made through https://jdhardware.shop and use of our website.",
    intro:
      "JD Hardware is operated by JD Hardware Co. Prices are displayed in pounds sterling, and delivery is currently within the United Kingdom.",
    groupTitles: [],
  },
  {
    slug: "cookie-policy",
    title: "Cookie Policy",
    description:
      "This Cookie Policy explains how JD Hardware may use cookies and similar technologies on https://jdhardware.shop.",
    intro:
      "Cookies are small text files that websites may store on a visitor's device.",
    groupTitles: [],
  },
  {
    slug: "legal-notice",
    title: "Legal Notice",
    description:
      "This Legal Notice provides information about the JD Hardware website and its operator.",
    intro: "JD Hardware is operated by JD Hardware Co.",
    groupTitles: ["General Questions"],
    paragraphs: [
      "Trading name: JD Hardware. Legal business name: JD Hardware Co. Website: https://jdhardware.shop.",
      "Business address: 280A Norwood Road, Norwood, London SE27 9AJ, United Kingdom. Email: info@jdhardware.shop. Telephone: 020 7606 3333. Live chat: 24/7.",
    ],
  },
  {
    slug: "accessibility-statement",
    title: "Accessibility Statement",
    description:
      "JD Hardware aims to provide an online shopping experience that is accessible to customers with different abilities and needs.",
    intro:
      "If a page, product listing, or checkout step is difficult to use, email info@jdhardware.shop or telephone 020 7606 3333. Live chat is available 24/7.",
    groupTitles: [],
  },
  {
    slug: "your-privacy-choices",
    title: "Your Privacy Choices",
    description:
      "JD Hardware recognises the importance of providing customers with information about their privacy rights.",
    intro:
      "This page explains the privacy choices that may be available under UK data protection law. Email info@jdhardware.shop with the subject line Privacy Rights Request.",
    groupTitles: [],
  },
];

export function policyBySlug(slug: string) {
  return POLICY_PAGES.find((page) => page.slug === slug) ?? null;
}

export function groupsForPolicy(policy: PolicyPageDef, groups: FaqGroup[]) {
  if (!policy.groupTitles.length) return [];
  return groups.filter((group) => policy.groupTitles.includes(group.title));
}

export function contentPageTitle(slug: string) {
  return CONTENT_PAGES.find((page) => page.slug === slug)?.title ?? slug;
}
