import '../styles/globals.css'
import '../styles/variables.css'

import Head from 'next/head'
import { VaporProvider } from '@vapor/ui';

function MyApp({ Component, pageProps }) {
  return (
    <VaporProvider>
      <Component {...pageProps} />

      <Head>
        <title>QVerify - Quantum Circuit Verification</title>
        <meta name="description" content="Equivalency verification for compiled quantum circuit" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
    </VaporProvider>
  )
}

export default MyApp
