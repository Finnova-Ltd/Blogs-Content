const FALLBACK_REVIEWS = [
  {
    author_name: 'n cassim',
    reviewer_meta: '10 reviews · 1 photo',
    relative_time_description: '4 months ago',
    rating: 5,
    text: 'From the start EZ Mortgage Broker guided us step by step and helped us in our financial matter. He took stock of our financial situation and gave us great pertinent advice. He did the heavy lifting at every step. Highly recommend EZ Mortgage Broker for personal and business financial matters. Well done EZ Mortgage Broker and all the best.',
    owner_response_time: '4 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Jaspreet Sidhu',
    reviewer_meta: '2 reviews',
    relative_time_description: '3 months ago',
    rating: 5,
    text: 'Hello everyone EZ Mortgage Broker helping me since 2018 for all my financial needs like first home buyer loan refinance every time they helped me a lot they are very professional, honest, reliable they know their job well they treat you like family.',
    owner_response_time: '3 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Navtej singh',
    reviewer_meta: '7 reviews',
    relative_time_description: '10 months ago',
    rating: 5,
    text: 'This is my second Time working with EZ Mortgage Broker to purchase my dream home. The entire journey was smooth and stress-free from start to finish. He guided me through every document and step of the process with great care. I truly appreciate his support and highly recommend his services.',
    owner_response_time: '10 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Emmy',
    reviewer_meta: '2 reviews',
    relative_time_description: '1 year ago',
    rating: 5,
    text: 'EZ Mortgage Broker has been an outstanding support throughout my entire loan process and that of my family. His professionalism, responsiveness, and dedication are unparalleled. Available 24/7, he worked exceptionally diligently to meet every one of my requirements.',
    owner_response_time: '1 year ago',
    owner_response_text: 'Thank you so much, Emily! I truly appreciate your kind words and support. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Madonna Health',
    reviewer_meta: '2 reviews',
    relative_time_description: 'Edited 11 months ago',
    rating: 5,
    text: 'Absolutely, Hyacinth! Here is a polished and professional review you could use.',
    owner_response_time: '1 year ago',
    owner_response_text: 'Thank you so much. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Justin Gray',
    reviewer_meta: '4 reviews',
    relative_time_description: '7 months ago',
    rating: 5,
    text: 'EZ Mortgage Broker has been fantastic throughout.',
    owner_response_time: '7 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Ajay Joshi',
    reviewer_meta: 'Local Guide · 22 reviews · 25 photos',
    relative_time_description: '3 months ago',
    rating: 5,
    text: 'Excellent service, recommended.',
    owner_response_time: '3 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'mohammed shameel',
    reviewer_meta: '7 reviews',
    relative_time_description: '1 year ago',
    rating: 5,
    text: 'Very professional service and great job done. Thank you pankaj sir.',
    owner_response_time: '1 year ago',
    owner_response_text: 'Thank you so much, Mohammed! I truly appreciate your kind words and support. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Manjula Rathnayaka',
    reviewer_meta: '1 review',
    relative_time_description: '1 year ago',
    rating: 5,
    text: 'Great job you done. Thank you EZ Mortgage Broker.',
    owner_response_time: '1 year ago',
    owner_response_text: 'Thank you so much, Manjula! I truly appreciate your kind words and support. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Harman Harry Singh',
    reviewer_meta: '4 reviews · 7 photos',
    relative_time_description: '1 year ago',
    rating: 5,
    text: 'Very good service and helpful all the way. Appreciate.',
    owner_response_time: '1 year ago',
    owner_response_text: 'Thank you so much, Harman! I truly appreciate your kind words and support. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Patel Ankitkumar Sunilbhai',
    reviewer_meta: '6 reviews',
    relative_time_description: '4 days ago',
    rating: 5,
    text: 'Easy and effective two way communication with EZ Mortgage Broker, hassle free process and documentation, every step of home loan process was handled carefully under the guidance of EZ Mortgage Broker.',
  },
  {
    author_name: 'Rod Wonnacott',
    reviewer_meta: '3 reviews',
    relative_time_description: '4 days ago',
    rating: 5,
    text: 'I found EZ Mortgage Broker to be very professional, friendly, supportive and efficient in securing finance for my business. They followed through on everything and consulted and informed excellently. I cannot recommend more highly.',
    owner_response_time: '4 days ago',
    owner_response_text: 'Thank you so much Rod for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Nikki Patel',
    reviewer_meta: '5 reviews',
    relative_time_description: '4 days ago',
    rating: 5,
    text: 'I would like to thank JM for their excellent service throughout my loan process. Everything was handled smoothly, clearly, and with great professionalism. The team was supportive, quick to respond, and made the entire experience stress free.',
    owner_response_time: '4 days ago',
    owner_response_text: 'Thank you so much Nikita for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
  {
    author_name: 'Amarinder Singh',
    reviewer_meta: '11 reviews · 2 photos',
    relative_time_description: '3 months ago',
    rating: 5,
    text: 'Five star service and support.',
    owner_response_time: '3 months ago',
    owner_response_text: 'Thank you so much for trusting me and my company. I truly appreciate your 5 star review. It was a pleasure working with you, and I am glad you were happy with the service. Do not hesitate to reach out if you ever need anything in the future.',
  },
];

const CACHE_TTL_SECONDS = 60 * 60 * 6;

function json(data, status = 200, cacheControl = 'public, max-age=600') {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': cacheControl,
    },
  });
}

function sanitizeReview(review = {}) {
  return {
    author_name: String(review.author_name || 'Anonymous').trim(),
    reviewer_meta: String(review.reviewer_meta || '').trim(),
    relative_time_description: String(review.relative_time_description || 'Recently').trim(),
    rating: Number(review.rating || 5),
    text: String(review.text || '').trim(),
    owner_response_time: String(review.owner_response_time || '').trim(),
    owner_response_text: String(review.owner_response_text || '').trim(),
  };
}

export async function onRequestGet(context) {
  const { env, request } = context;

  try {
    const useFallback = String(env.GOOGLE_REVIEWS_FALLBACK_ONLY || '').toLowerCase() === 'true';
    const placeId = env.GOOGLE_PLACE_ID;
    const apiKey = env.GOOGLE_PLACES_API_KEY;

    if (useFallback || !placeId || !apiKey) {
      return json({
        source: 'fallback',
        placeName: 'EZ MORTGAGE BROKER',
        rating: 5,
        userRatingsTotal: 14,
        reviews: FALLBACK_REVIEWS,
      });
    }

    const edgeCache = caches.default;
    const edgeCacheKey = new Request(request.url, { method: 'GET' });
    const edgeHit = await edgeCache.match(edgeCacheKey);
    if (edgeHit) {
      return edgeHit;
    }

    const cacheKey = `google-reviews:${placeId}`;
    const now = Date.now();

    if (env.REVIEWS_CACHE) {
      const cachedRaw = await env.REVIEWS_CACHE.get(cacheKey);
      if (cachedRaw) {
        const cached = JSON.parse(cachedRaw);
        if (cached.expiresAt && cached.expiresAt > now) {
          return json({ ...cached.payload, source: 'cache' }, 200, 'public, max-age=900');
        }
      }
    }

    const url = new URL('https://maps.googleapis.com/maps/api/place/details/json');
    url.searchParams.set('place_id', placeId);
    url.searchParams.set('fields', 'name,rating,user_ratings_total,reviews,url');
    url.searchParams.set('reviews_sort', 'newest');
    url.searchParams.set('key', apiKey);

    const fetchRes = await fetch(url.toString(), {
      headers: { Accept: 'application/json' },
    });

    if (!fetchRes.ok) {
      throw new Error(`Google API error: ${fetchRes.status}`);
    }

    const payload = await fetchRes.json();

    if (payload.status !== 'OK') {
      throw new Error(payload.error_message || payload.status || 'Unknown Google Places error');
    }

    const result = payload.result || {};
    const reviews = Array.isArray(result.reviews)
      ? result.reviews.map(sanitizeReview).filter((item) => item.text)
      : [];

    const finalPayload = {
      source: 'google',
      placeName: result.name || 'EZ MORTGAGE BROKER',
      rating: Number(result.rating || 5),
      userRatingsTotal: Number(result.user_ratings_total || reviews.length || 0),
      googleUrl: result.url || null,
      reviews: reviews.length ? reviews : FALLBACK_REVIEWS,
    };

    if (env.REVIEWS_CACHE) {
      await env.REVIEWS_CACHE.put(
        cacheKey,
        JSON.stringify({
          expiresAt: now + CACHE_TTL_SECONDS * 1000,
          payload: finalPayload,
        }),
        {
          expirationTtl: CACHE_TTL_SECONDS,
        }
      );
    }

    const response = json(finalPayload, 200, 'public, max-age=900');
    context.waitUntil(edgeCache.put(edgeCacheKey, response.clone()));
    return response;
  } catch (error) {
    return json(
      {
        source: 'fallback',
        warning: error instanceof Error ? error.message : 'Failed to fetch Google reviews',
        placeName: 'EZ MORTGAGE BROKER',
        rating: 5,
        userRatingsTotal: 14,
        reviews: FALLBACK_REVIEWS,
      },
      200,
      'public, max-age=300'
    );
  }
}
