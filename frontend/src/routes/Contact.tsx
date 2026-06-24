import ContactForm from '../components/ContactForm';

export default function Contact() {
  return (
    <section>
      <h1>Contact</h1>
      <ContactForm onSubmit={(data) => console.log('submitted', data)} />
    </section>
  );
}
