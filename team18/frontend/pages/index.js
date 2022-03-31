import { useState, useEffect } from 'react';
import { styled } from 'buttered';
import { Button, Textarea } from '@vapor/ui';
import { ArrowRight } from 'react-feather';

import dynamic from 'next/dynamic'

const DynamicComponentWithNoSSR = dynamic(() =>
  import('../components/editor').then(mod => mod.Editor),
  { ssr: false }
)

let Wrapper = styled('div')`
  display: grid;
  grid-template-columns: 1fr 1fr;

  @media screen and (max-width: 800px) {
    grid-template-columns: 1fr;
  }
`;

let LeftWrapper = styled('div')`
  min-height: 100vh;
  border-right: 1px solid var(--vapor-accent-9);
`;

let RightWrapper = styled('div')`
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
`;

let EditorWrapper = styled('div')`
  min-height: 100vh;
  background: var(--vapor-background);
  padding: 60px 0;
  padding-left: -5px;
  display: flex;
  justify-content: center;
`;

let DigitalLogicCircuitWrapper = styled('div')`
  background: var(--vapor-background);
  border-bottom: 1px solid var(--vapor-accent-8);
`;

let VerificationWrapper = styled('div')`
  background: var(--vapor-background);
  border-bottom: 1px solid var(--vapor-accent-8);
`;

let BasisGateCircuitWrapper = styled('div')`
  background: var(--vapor-background);
`;

export default function Home() {
  let [value, setValue] = useState("");

  let onEditorChange = (newValue) => {
    setValue(newValue);
  }

  useEffect(() => {

  }, []);

  return (
    <Wrapper>
      <LeftWrapper>
        <EditorWrapper>
          <DynamicComponentWithNoSSR
            value={value}
            onChange={onEditorChange}
          />
        </EditorWrapper>
      </LeftWrapper>

      <RightWrapper>
        <DigitalLogicCircuitWrapper></DigitalLogicCircuitWrapper>

        <VerificationWrapper></VerificationWrapper>

        <BasisGateCircuitWrapper></BasisGateCircuitWrapper>
      </RightWrapper>
    </Wrapper>
  )
}
