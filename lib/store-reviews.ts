import type { GenericReview } from "@/lib/types";

const PLACES = [
  ["Greater London", "London"],
  ["Greater Manchester", "Manchester"],
  ["West Midlands", "Birmingham"],
  ["West Yorkshire", "Leeds"],
  ["Bristol", "Bristol"],
  ["Glasgow", "Glasgow"],
  ["Cardiff", "Cardiff"],
  ["Merseyside", "Liverpool"],
  ["Edinburgh", "Edinburgh"],
  ["South Yorkshire", "Sheffield"],
  ["Nottinghamshire", "Nottingham"],
  ["Belfast", "Belfast"],
  ["Tyne and Wear", "Newcastle"],
  ["Hampshire", "Southampton"],
  ["Kent", "Canterbury"],
  ["Leicestershire", "Leicester"],
  ["East Sussex", "Brighton"],
  ["Oxfordshire", "Oxford"],
  ["Cambridgeshire", "Cambridge"],
  ["Devon", "Exeter"],
  ["Norfolk", "Norwich"],
  ["Aberdeen", "Aberdeen"],
  ["Swansea", "Swansea"],
  ["Derry", "Derry"],
] as const;

const FIRST = [
  "Amina", "James", "Sofia", "Daniel", "Priya", "Noah", "Elena", "Omar",
  "Maya", "Chris", "Lina", "Theo", "Hannah", "Marcus", "Grace", "Andre",
  "Chloe", "Ryan", "Fatima", "Owen", "Natalie", "Jamal", "Brooke", "Ethan",
  "Lucia", "Colin", "Aisha", "Patrick", "Megan", "Luis", "Harper", "Derek",
  "Nina", "Caleb", "Rosa", "Ian", "Kelly", "Victor", "Ava", "Samir",
];

const LAST = "ABCDEFGHJKLMNPRSTW".split("");

const PRODUCTS = [
  "hedge trimmer",
  "pressure washer",
  "garden arch",
  "wood stove",
  "computer monitor",
  "leaf blower",
  "porch swing",
  "chainsaw",
  "greenhouse",
  "log rack",
  "power tiller",
];

const TITLES_5 = [
  "Packed with care",
  "Would order again",
  "Matched the listing",
  "Smooth checkout",
  "Arrived ready to use",
  "Clear tracking",
  "Well made and well packed",
  "Easy order",
  "Photos matched the page",
  "Glad we chose this shop",
];

const TITLES_4 = [
  "Good order",
  "Happy overall",
  "Solid buy",
  "Worth ordering",
  "Quality was there",
  "Would recommend",
];

function fiveStarNote(product: string, city: string, state: string, index: number) {
  const notes = [
    `Bought a ${product} for our home in ${city}, ${state}. It was packed carefully and matched the listing.`,
    `My ${product} arrived in ${city} on time. Checkout was clear and the box arrived in good shape.`,
    `Needed a ${product} here in ${state}. Tracking was easy to follow and it was ready to use.`,
    `Our ${product} showed up in ${city} exactly as described. I would order from them again.`,
    `Placed an order for a ${product} while in ${state}. The price was fair and the shipping updates were useful.`,
    `The ${product} I ordered for ${city} feels well made. Support answered a question the same day.`,
    `Shopping from ${state} was straightforward. The ${product} was packed securely and the photos were accurate.`,
    `Gave a ${product} as a gift in ${city}. The packaging looked neat and the order was simple to place.`,
  ];
  return notes[index % notes.length];
}

function fourStarNote(product: string, city: string, state: string, index: number) {
  const notes = [
    `The ${product} is good quality. Delivery to ${city}, ${state} took a day longer than the first estimate.`,
    `Happy with my order in ${state}. The ${product} does the job. Shipping to ${city} was a little slower than I hoped.`,
    `Solid ${product} for the price. I was kept updated on the way to ${city}.`,
    `I would recommend the shop to someone in ${state}. The ${product} arrived safely, just not on the first promised day.`,
  ];
  return notes[index % notes.length];
}

function dateFor(index: number) {
  const day = new Date(Date.UTC(2026, 8, 20));
  day.setUTCDate(day.getUTCDate() - index * 3);
  return day.toISOString().slice(0, 10);
}

/** 77 five-star and 33 four-star notes. 517 / 110 = 4.7. */
function buildStoreReviews(): GenericReview[] {
  const ratings = [
    ...Array.from({ length: 77 }, () => 5),
    ...Array.from({ length: 33 }, () => 4),
  ];

  return ratings.map((rating, index) => {
    const [state, city] = PLACES[index % PLACES.length];
    const first = FIRST[index % FIRST.length];
    const last = LAST[(index * 3) % LAST.length];
    const product = PRODUCTS[index % PRODUCTS.length];
    const five = rating === 5;
    const titles = five ? TITLES_5 : TITLES_4;
    return {
      reviewer: `${first} ${last}.`,
      rating,
      title: titles[index % titles.length],
      content: five
        ? fiveStarNote(product, city, state, index)
        : fourStarNote(product, city, state, index),
      date: dateFor(index),
      verified: true,
      location: `${city}, ${state}, United Kingdom`,
    };
  });
}

let cachedReviews: GenericReview[] | null = null;

export function storeReviews(): GenericReview[] {
  cachedReviews ??= buildStoreReviews();
  return cachedReviews;
}

export function storeReviewSummary() {
  const reviews = storeReviews();
  const total = reviews.length;
  const average =
    total > 0
      ? reviews.reduce((sum, review) => sum + review.rating, 0) / total
      : 0;
  const states = new Set(
    reviews.map((review) => review.location?.split(",")[1]?.trim() || ""),
  );
  return {
    total,
    average,
    stateCount: states.size,
  };
}
