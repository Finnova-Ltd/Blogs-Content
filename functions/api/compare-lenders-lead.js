const REQUIRED_FIELDS = ['intent', 'firstName', 'mobile'];

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

    for (const field of REQUIRED_FIELDS) {
      if (!String(body[field] || '').trim()) {
        return badRequest(`Missing required field: ${field}`);
      }
    }

    const mobileDigits = String(body.mobile || '').replace(/\D/g, '');
    if (mobileDigits.length < 9) {
      return badRequest('Please provide a valid Australian mobile phone number.');
    }

    if (!env.RESEND_API_KEY) {
      return Response.json({ error: 'Missing RESEND_API_KEY environment variable.' }, { status: 500 });
    }

    const fromEmail = env.RESEND_FROM_EMAIL || 'JM Loans <no-reply@jmloans.com.au>';
    const brokerEmail = env.BROKER_EMAIL || 'info@jmloans.com.au';

    const lenderPriorities = Array.isArray(body.lenderPriorities)
      ? body.lenderPriorities.map((item) => String(item)).join(', ')
      : '';

    const rows = [
      ['Intent', body.intent],
      ['Loan Balance', body.loanBalance],
      ['Purchase Price', body.purchasePrice],
      ['Deposit', body.deposit],
      ['Buying Situation', body.buySituation],
      ['First Home Buyer', body.firstHomeBuyer],
      ['Property Type', body.propertyType],
      ['Property Use', body.propertyUse],
      ['Lender Priorities', lenderPriorities],
      ['Credit History', body.creditHistory],
      ['Income Type', body.incomeType],
      ['First Name', body.firstName],
      ['Mobile', body.mobile],
      ['Source', body.source],
      ['Submitted At', body.submittedAt],
    ]
      .filter(([, value]) => String(value || '').trim())
      .map(
        ([key, value]) => `
          <tr>
            <td style="padding:8px 10px;border:1px solid #d7e2f1;font-weight:700">${escapeHtml(key)}</td>
            <td style="padding:8px 10px;border:1px solid #d7e2f1">${escapeHtml(value)}</td>
          </tr>
        `
      )
      .join('');

    const emailResponse = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: fromEmail,
        to: [brokerEmail],
        subject: `JM Loans lead captured - ${body.intent || 'Compare Lenders'}`,
        html: `
          <div style="font-family:Arial,sans-serif;color:#17324b">
            <h2 style="margin:0 0 10px">Compare Lenders Lead</h2>
            <p style="margin:0 0 12px">A new compare-lenders form submission was received.</p>
            <table style="border-collapse:collapse;width:100%;max-width:780px">
              ${rows}
            </table>
          </div>
        `,
      }),
    });

    const payload = await emailResponse.json().catch(() => ({}));

    if (!emailResponse.ok) {
      return Response.json({ error: payload?.message || 'Failed to submit lead.' }, { status: 502 });
    }

    return Response.json({ ok: true, id: payload?.id || null });
  } catch (error) {
    return Response.json(
      {
        error: error instanceof Error ? error.message : 'Unexpected server error.',
      },
      { status: 500 }
    );
  }
}
