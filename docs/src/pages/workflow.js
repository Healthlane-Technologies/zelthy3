import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import ZelthyLandingPageBgImg from '/img/zelthy_landing_pg_bg.jpg';

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <Layout
      title={`Workflow Package`}
      description="Workflow Package">
      <main>
      <iframe
        style={{height: '100vh'}}
        title="Embedded Content"
        width="100%"
        height="100vh"
        src="https://docs.zelthy.com/workflow1/docs/documentation/overview/"
        frameBorder="0"
        allowFullScreen
      ></iframe>
      </main>
    </Layout>
  );
}
