/**
 * Vercel Serverless API Route: /api/send-score
 * Securely forwards student mock test score notifications to Telegram API
 */

export default async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { botToken, chatId, message } = req.body || {};

    // Use token/chatId from request body OR fallback to server environment variables
    const finalToken = botToken || process.env.TELEGRAM_BOT_TOKEN;
    const finalChatId = chatId || process.env.TELEGRAM_CHAT_ID;

    if (!finalToken || !finalChatId) {
      return res.status(400).json({ 
        error: 'Missing Telegram credentials. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables or configure in app.' 
      });
    }

    // Call Telegram Bot API
    const tgUrl = `https://api.telegram.org/bot${finalToken}/sendMessage`;
    const tgResponse = await fetch(tgUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: finalChatId,
        text: message,
        parse_mode: 'Markdown'
      })
    });

    const data = await tgResponse.json();

    if (!tgResponse.ok || !data.ok) {
      console.error('Telegram API Error:', data);
      return res.status(500).json({ 
        error: 'Telegram API Error', 
        details: data.description || 'Unknown error' 
      });
    }

    return res.status(200).json({ 
      success: true, 
      message: 'Score report sent to Telegram successfully' 
    });

  } catch (err) {
    console.error('Serverless function error:', err);
    return res.status(500).json({ error: 'Internal Server Error', message: err.message });
  }
}
