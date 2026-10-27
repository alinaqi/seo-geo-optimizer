export default function Pricing() {
  return (
    <main>
      <h1>Pricing</h1>
      <h2>Plans</h2>
      <p>It depends on what you need. In this page we will talk about our plans. They are flexible and this helps teams of all sizes.</p>
      <h2>FAQ</h2>
      <p>This is where we answer things. It is simple.</p>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: [{ '@type': 'Question', name: 'Is there a free trial?', acceptedAnswer: { '@type': 'Answer', text: 'Yes, 14 days.' } }] }) }} />
    </main>
  );
}
