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

    const fullName = body.full_name || body.name || ((body.first_name || '') + ' ' + (body.last_name || '')).trim() || 'Anonymous Applicant';
    const mobile = body.mobile_number || body.phone || body.mobile || '';
    const email = body.email_address || body.email || '';
    const postcode = body.postcode || body.post_code || '3004';
    const loanPurpose = body.loan_purpose || body.goal || body.purpose || body.intent || 'Mortgage Consultation';
    const buyerType = body.buyer_type || body.buyerType || '';
    const incomeSource = body.income_source || body.incomeSource || '';
    const estimatedAmount = body.estimated_amount || body.propertyValue || body.loanBalance || body.amount || 'Not specified';
    const message = body.description || body.message || '';
    const formName = body.form_name || body.formName || 'Website Enquiry';
    const sourceUrl = body.source_url || body.source || request.headers.get('referer') || 'https://ezmortgagebroker.com.au';
    const submittedAt = new Date().toLocaleString('en-AU', { timeZone: 'Australia/Melbourne' }) + ' (AEST)';

    if (!mobile && !email) {
      return badRequest('Please provide at least a phone number or email address.');
    }

    const leadId = 'lead_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7);

    // Primary Notification Target: info@ezmortgagebroker.com.au
    const brokerEmail = env.BROKER_EMAIL || 'info@ezmortgagebroker.com.au';
    const fromEmail = env.RESEND_FROM_EMAIL || 'EZ Mortgage Broker <no-reply@ezmortgagebroker.com.au>';

    // If Resend API Key is configured in Cloudflare Environment, dispatch notification email
    if (env.RESEND_API_KEY) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${env.RESEND_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: fromEmail,
            to: [brokerEmail],
            reply_to: email || undefined,
            subject: `🎯 New Lead: ${fullName} (${loanPurpose})`,
            html: `
              <div style="font-family:Arial,sans-serif;color:#0A2540;max-width:620px;margin:0 auto;border:1.5px solid #E2E8F0;border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.06);">
                <div style="background:#0A2540;color:#ffffff;padding:20px 24px;">
                  <h2 style="margin:0;font-size:20px;color:#FFDC4A;">🎯 New Website Lead Captured</h2>
                  <p style="margin:4px 0 0;font-size:13px;color:#E2E8F0;">EZ Mortgage Broker Lead Notification System</p>
                </div>
                <div style="padding:24px;">
                  <table style="width:100%;border-collapse:collapse;font-size:14px;line-height:1.6;">
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;width:35%;">Applicant Name:</td><td style="font-weight:bold;color:#0A2540;">${escapeHtml(fullName)}</td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Mobile Phone:</td><td><a href="tel:${escapeHtml(mobile)}" style="color:#1D4ED8;font-weight:bold;text-decoration:none;">${escapeHtml(mobile)}</a></td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Email Address:</td><td><a href="mailto:${escapeHtml(email)}" style="color:#1D4ED8;font-weight:bold;text-decoration:none;">${escapeHtml(email)}</a></td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Postcode / Location:</td><td>${escapeHtml(postcode)}</td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Loan Goal:</td><td><span style="background:#EFF6FF;color:#1D4ED8;padding:3px 8px;border-radius:4px;font-weight:bold;">${escapeHtml(loanPurpose)}</span></td></tr>
                    ${buyerType ? `<tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Buyer Type:</td><td>${escapeHtml(buyerType)}</td></tr>` : ''}
                    ${incomeSource ? `<tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Income Source:</td><td>${escapeHtml(incomeSource)}</td></tr>` : ''}
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Property / Loan Value:</td><td>${escapeHtml(estimatedAmount)}</td></tr>
                    ${message ? `<tr><td style="padding:8px 0;font-weight:bold;color:#64748B;vertical-align:top;">Message / Notes:</td><td><div style="background:#F8FAFC;padding:10px 12px;border-radius:6px;border:1px solid #E2E8F0;">${escapeHtml(message)}</div></td></tr>` : ''}
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Form Source:</td><td>${escapeHtml(formName)}</td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Source URL:</td><td><a href="${escapeHtml(sourceUrl)}" style="color:#64748B;font-size:12px;">${escapeHtml(sourceUrl)}</a></td></tr>
                    <tr><td style="padding:8px 0;font-weight:bold;color:#64748B;">Submitted At:</td><td style="color:#64748B;font-size:12px;">${submittedAt}</td></tr>
                  </table>
                  <div style="margin-top:24px;padding-top:16px;border-top:1px solid #F1F5F9;text-align:center;">
                    <a href="tel:${escapeHtml(mobile)}" style="display:inline-block;background:#00876C;color:#ffffff;font-weight:bold;padding:10px 20px;border-radius:6px;text-decoration:none;margin-right:10px;">📞 Call Applicant Now</a>
                    <a href="mailto:${escapeHtml(email)}" style="display:inline-block;background:#0A2540;color:#ffffff;font-weight:bold;padding:10px 20px;border-radius:6px;text-decoration:none;">✉️ Reply via Email</a>
                  </div>
                </div>
                <div style="background:#F8FAFC;padding:12px 24px;font-size:11px;color:#94A3B8;text-align:center;border-top:1px solid #E2E8F0;">
                  Mortgage Broker Online Pty Ltd (trading as EZ Mortgage Broker) | 470 St Kilda Rd, Melbourne VIC 3004
                </div>
              </div>
            `,
          }),
        });
      } catch (err) {
        console.error('Email dispatch error:', err);
      }
    }

    return Response.json({
      ok: true,
      success: true,
      leadId: leadId,
      sent_to: brokerEmail,
      message: 'Assessment request successfully submitted and forwarded to info@ezmortgagebroker.com.au.',
    });
  } catch (error) {
    return Response.json(
      {
        error: error instanceof Error ? error.message : 'Unexpected server error.',
      },
      { status: 500 }
    );
  }
}
