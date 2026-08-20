function badRequest(message) {
  return Response.json({ error: message }, { status: 400 });
}

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const body = await request.json();
    const { name, email, turnstileToken, submittedAt } = body;

    if (!String(name || '').trim()) {
      return badRequest('Name is required.');
    }
    if (!String(email || '').trim() || !email.includes('@')) {
      return badRequest('Valid email address is required.');
    }

    // Verify Cloudflare Turnstile Token if secret key configured
    if (env.TURNSTILE_SECRET_KEY && turnstileToken) {
      const verifyRes = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          secret: env.TURNSTILE_SECRET_KEY,
          response: turnstileToken,
        }),
      });

      const verifyData = await verifyRes.json().catch(() => ({}));
      if (!verifyData.success) {
        return badRequest('Cloudflare Turnstile verification failed. Please try again.');
      }
    }

    // Send notification email via Resend if configured
    if (env.RESEND_API_KEY) {
      const fromEmail = env.RESEND_FROM_EMAIL || 'JM Loans <no-reply@jmloans.com.au>';
      const brokerEmail = env.BROKER_EMAIL || 'info@jmloans.com.au';

      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: fromEmail,
          to: [brokerEmail],
          subject: `New Newsletter Subscriber - ${escapeHtml(name)}`,
          html: `
            <div style="font-family:Arial,sans-serif;color:#17324b">
              <h2 style="margin:0 0 10px">New Stay Connected Newsletter Subscriber</h2>
              <p style="margin:0 0 12px">A new visitor subscribed to the newsletter:</p>
              <table style="border-collapse:collapse;width:100%;max-width:500px">
                <tr>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1;font-weight:700">Name</td>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1">${escapeHtml(name)}</td>
                </tr>
                <tr>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1;font-weight:700">Email</td>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1">${escapeHtml(email)}</td>
                </tr>
                <tr>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1;font-weight:700">Submitted At</td>
                  <td style="padding:8px 10px;border:1px solid #d7e2f1">${escapeHtml(submittedAt || new Date().toISOString())}</td>
                </tr>
              </table>
            </div>
          `,
        }),
      });
    }

    // Forward to Directus CMS if DIRECTUS_URL configured
    if (env.DIRECTUS_URL) {
      try {
        const directusUrl = `${env.DIRECTUS_URL.replace(/\/$/, '')}/items/subscribers`;
        const headers = { 'Content-Type': 'application/json' };
        if (env.DIRECTUS_STATIC_TOKEN) {
          headers['Authorization'] = `Bearer ${env.DIRECTUS_STATIC_TOKEN}`;
        }
        await fetch(directusUrl, {
          method: 'POST',
          headers,
          body: JSON.stringify({ name, email, created_at: submittedAt || new Date().toISOString() }),
        });
      } catch (directusErr) {
        console.error('Directus forwarding error:', directusErr);
      }
    }

    return Response.json({ ok: true, message: 'Subscribed successfully.' });
  } catch (err) {
    return Response.json(
      { error: err instanceof Error ? err.message : 'Internal server error' },
      { status: 500 }
    );
  }
}
