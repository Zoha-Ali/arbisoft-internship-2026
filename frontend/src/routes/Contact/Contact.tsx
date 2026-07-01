import ContactForm from '../../components/ContactForm/ContactForm';

const Contact = () => {
  return (
    <section>
      <h1>Contact</h1>
      <ContactForm onSubmit={(data) => console.log('submitted', data)} />
    </section>
  );
};

export default Contact;
