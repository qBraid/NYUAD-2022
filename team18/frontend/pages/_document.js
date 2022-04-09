import Document, { Html, Head, Main, NextScript } from 'next/document';
import { getServerCss } from '@vapor/ui';

export default class MyDocument extends Document {
  static async getInitialProps({ renderPage }) {
    let page = await renderPage();
    let css = getServerCss();

    return { ...page, css };
  }

  render() {
    return (
      <Html lang="en">
        <Head>
          <style
            id="buttered"
            dangerouslySetInnerHTML={{ __html: ' ' + this.props.css }}
          />

          <link rel="stylesheet" href="/inter/index.css" />
        </Head>

        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}