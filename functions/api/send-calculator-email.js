export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const body = await request.json();
    const fullName = (body.fullName || '').trim();
    const email = (body.email || '').trim();
    const phone = (body.phone || '').trim();
    const postcode = (body.postcode || '3029').trim();
    const calculatorTitle = (body.calculatorTitle || 'Calculator').trim();
    const summaryData = body.summaryData || {};
    const turnstileToken = body.turnstileToken;

    if (!email) {
      return Response.json({ error: 'Email address is required.' }, { status: 400 });
    }

    // Verify Cloudflare Turnstile token if Turnstile secret key is configured
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
        return Response.json({ error: 'Cloudflare Turnstile verification failed. Please try again.' }, { status: 400 });
      }
    }

    // Format summary rows
    const summaryHtml = Object.entries(summaryData)
      .map(([k, v]) => `<tr><td style="padding:6px 12px;border:1px solid #e2e8f0;font-weight:600;">${k}</td><td style="padding:6px 12px;border:1px solid #e2e8f0;font-weight:700;color:#00a896;">${v}</td></tr>`)
      .join('');

    // Send email via Resend if key exists
    if (env.RESEND_API_KEY) {
      const fromEmail = env.RESEND_FROM_EMAIL || 'EZ Mortgage Broker <no-reply@ezmortgagebroker.com.au>';
      const brokerEmail = env.BROKER_EMAIL || 'info@ezmortgagebroker.com.au';
      const subject = `EZ Mortgage Broker - ${calculatorTitle} Summary`;

      // Email to Client User
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: fromEmail,
          to: [email],
          subject,
          html: `
            <div style="font-family:Arial,sans-serif;line-height:1.6;color:#16324b;max-width:600px;margin:0 auto;border:1px solid #e2e8f0;border-radius:8px;padding:24px;">
              <h2 style="color:#09233c;margin:0 0 12px;">EZ Mortgage Broker</h2>
              <p>Hi <strong>${fullName || 'there'}</strong>,</p>
              <p>Here is your calculation summary from <strong>${calculatorTitle}</strong>:</p>
              <table style="width:100%;border-collapse:collapse;margin:16px 0;">
                <tbody>${summaryHtml}</tbody>
              </table>
              <p>Our principal broker EZ Mortgage Broker in Victoria will review your figures and contact you shortly with competitive loan options.</p>
              <hr style="border:none;border-top:1px solid #e2e8f0;margin:20px 0;" />
              <p style="font-size:12px;color:#64748b;">JM Loans Pty Ltd | Credit Representative Number 479386 | info@ezmortgagebroker.com.au</p>
            </div>
          `,
        }),
      });

      // Email Notification to Broker (info@ezmortgagebroker.com.au)
      await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: fromEmail,
          to: [brokerEmail],
          subject: `🔥 New Lead: ${fullName} (${calculatorTitle})`,
          html: `
            <div style="font-family:Arial,sans-serif;line-height:1.6;color:#16324b;">
              <h2>New Calculator Lead Captured</h2>
              <p><strong>Name:</strong> ${fullName}</p>
              <p><strong>Email:</strong> ${email}</p>
              <p><strong>Phone:</strong> ${phone}</p>
              <p><strong>Postcode:</strong> ${postcode}</p>
              <p><strong>Calculator:</strong> ${calculatorTitle}</p>
              <h3>Calculation Details:</h3>
              <table style="width:100%;border-collapse:collapse;">
                <tbody>${summaryHtml}</tbody>
              </table>
            </div>
          `,
        }),
      });
    }

    // Directus Forwarding if configured
    if (env.DIRECTUS_URL) {
      try {
        const directusUrl = `${env.DIRECTUS_URL.replace(/\/$/, '')}/items/leads`;
        const headers = { 'Content-Type': 'application/json' };
        if (env.DIRECTUS_STATIC_TOKEN) {
          headers['Authorization'] = `Bearer ${env.DIRECTUS_STATIC_TOKEN}`;
        }
        await fetch(directusUrl, {
          method: 'POST',
          headers,
          body: JSON.stringify({
            full_name: fullName,
            email,
            phone,
            postcode,
            calculator: calculatorTitle,
            summary_json: JSON.stringify(summaryData),
            notes: body.notes || '',
            created_at: new Date().toISOString(),
          }),
        });
      } catch (err) {
        console.error('Directus forwarding error:', err);
      }
    }

    return Response.json({ success: true, message: 'Calculation summary sent successfully.' });
  } catch (error) {
    return Response.json({ error: error.message || 'Failed to send calculator summary email.' }, { status: 500 });
  }
}
