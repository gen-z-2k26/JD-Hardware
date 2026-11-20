import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { feedStoreOrigin, PUBLIC_STORE_ORIGIN, rewriteProductLinks } from "./ctx-feed.ts";

const item = `<item>
<link><![CDATA[https://wp.jdhardware.shop/product/garden-arch/]]></link>
<g:image_link><![CDATA[https://wp.jdhardware.shop/wp-content/uploads/2026/11/1.jpg]]></g:image_link>
<g:canonical_link><![CDATA[https://wp.jdhardware.shop/product/garden-arch/]]></g:canonical_link>
</item>`;

describe("CTX feed links", () => {
  it("uses jdhardware.shop when the public URL is the WordPress host", () => {
    assert.equal(
      feedStoreOrigin("https://wp.jdhardware.shop", "https://wp.jdhardware.shop"),
      PUBLIC_STORE_ORIGIN,
    );
    assert.equal(
      feedStoreOrigin("https://wp.jdhardware.shop", "https://jdhardware.shop"),
      PUBLIC_STORE_ORIGIN,
    );
    assert.equal(
      feedStoreOrigin("https://wp.jdhardware.shop", "https://www.jdhardware.shop"),
      PUBLIC_STORE_ORIGIN,
    );
  });

  it("keeps a non-production storefront origin", () => {
    assert.equal(
      feedStoreOrigin("https://wp.jdhardware.shop", "http://localhost:3000"),
      "http://localhost:3000",
    );
  });

  it("rewrites product and home links and leaves images on WordPress", () => {
    const xml = `<channel><link><![CDATA[ https://wp.jdhardware.shop ]]></link>${item}</channel>`;
    const out = rewriteProductLinks(xml, "https://wp.jdhardware.shop", PUBLIC_STORE_ORIGIN);
    assert.match(out, /<link>https:\/\/jdhardware\.shop\/<\/link>/);
    assert.match(
      out,
      /<link>https:\/\/jdhardware\.shop\/products\/garden-arch<\/link>/,
    );
    assert.match(
      out,
      /<g:canonical_link>https:\/\/jdhardware\.shop\/products\/garden-arch<\/g:canonical_link>/,
    );
    assert.match(out, /wp\.jdhardware\.shop\/wp-content\/uploads/);
    assert.equal(out.includes("/product/"), false);
  });
});
