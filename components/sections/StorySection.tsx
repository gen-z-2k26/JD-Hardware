import Image from "next/image";
import Link from "next/link";
import type { StoreSettings } from "@/lib/types";
import { Reveal, RevealImage } from "@/components/sections/Reveal";
import { buttonVariants } from "@/components/ui/button";
import { pageContainer, sectionYClass } from "@/lib/layout";
import { cn } from "@/lib/utils";

export function StorySection({ settings }: { settings: StoreSettings }) {
  return (
    <section
      aria-labelledby="story-heading"
      className={cn("border-b border-border", sectionYClass)}
    >
      <div
        className={pageContainer(
          "grid items-center gap-8 lg:grid-cols-2 lg:gap-14",
        )}
      >
        <RevealImage className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-muted">
          <Image
            src="/brand/collection-climate.jpg"
            alt="Bright living room"
            fill
            sizes="(min-width: 1024px) 40vw, 100vw"
            className="object-cover"
          />
        </RevealImage>

        <Reveal className="space-y-5">
          <p className="text-sm font-medium tracking-[0.16em] text-accent uppercase">
            About {settings.name}
          </p>
          <h2
            id="story-heading"
            className="font-display text-balance text-3xl sm:text-4xl"
          >
            A clearer way to shop for home and garden
          </h2>
          <p className="text-pretty text-lg leading-relaxed text-muted-foreground">
            {settings.name} is a UK online shop for lawn and garden, outdoor
            power, heating, home improvement, and electronics, operated by{" "}
            {settings.contact.legalName} in London.
          </p>
          <ul className="space-y-3 text-sm leading-relaxed text-muted-foreground">
            <li>Product details, prices in pounds, and delivery estimates shown before checkout.</li>
            <li>Free standard UK delivery, with tracking when a shipment is created.</li>
            <li>
              Customer care at {settings.contact.email} or {settings.contact.phone}. Live chat is available 24/7.
            </li>
          </ul>
          <div className="flex flex-wrap gap-3 pt-2">
            <Link href="/about-us" className={cn(buttonVariants({ size: "lg" }))}>
              About us
            </Link>
            <Link
              href="/our-commitment"
              className={cn(buttonVariants({ size: "lg", variant: "outline" }))}
            >
              Our commitment
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
