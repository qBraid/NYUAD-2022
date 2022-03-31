import { useState } from 'react';
import { styled } from 'buttered';

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
  display: grid;
  grid-template-rows: 2fr 1fr;

  border-right: 1px solid var(--vapor-accent-9);
  background: var(--vapor-background);
`;

let RightWrapper = styled('div')`
  display: grid;
  grid-template-rows: 1fr 1fr 1fr;
`;

let EditorWrapper = styled('div')`
  display: flex;
  justify-content: center;
  align-items: center; 
  border-bottom: 1px solid var(--vapor-accent-8);
`;

let Button = styled('div')`
  display: flex;
  justify-content: center;
  align-items: center; 
  color: white;
  font-weight: 600;
  font-size: 32px;
  background: var(--vapor-foreground);
  
  &:hover {
    cursor: pointer;
  }
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

  let onClickCompile = () => {
    console.log(value);
  }

  return (
    <Wrapper>
      <LeftWrapper>
        <EditorWrapper>
          <DynamicComponentWithNoSSR
            value={value}
            onChange={onEditorChange}
          />
        </EditorWrapper>

        <Button onClick={onClickCompile}>
          Compile and Verify
        </Button>
      </LeftWrapper>

      <RightWrapper>
        <DigitalLogicCircuitWrapper></DigitalLogicCircuitWrapper>

        <VerificationWrapper></VerificationWrapper>

        <BasisGateCircuitWrapper></BasisGateCircuitWrapper>
      </RightWrapper>
    </Wrapper>
  )
}
