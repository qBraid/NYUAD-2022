import { useState } from 'react';
import { styled } from 'buttered';
import axios from 'axios';

import dynamic from 'next/dynamic'

import { Images } from './images.js'

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

let ImageComponent = styled('img')`
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
  let [code, setCode] = useState("");

  let onEditorChange = (newCode) => {
    setCode(newCode);
  }

  let onClickCompile = async () => {
    let payload = { code }

    axios.post(`http://127.0.0.1:5000/`, payload).then(res => {
      console.log(res);

      // here stuff has to happen
    });
  }

  return (
    <Wrapper>
      <LeftWrapper>
        <EditorWrapper>
          <DynamicComponentWithNoSSR
            value={code}
            onChange={onEditorChange}
          />
        </EditorWrapper>

        <Button onClick={onClickCompile}>
          Compile and Verify
        </Button>
      </LeftWrapper>

      <RightWrapper>
        <DigitalLogicCircuitWrapper>
          <ImageComponent src={"/placeHolder.png"} />
        </DigitalLogicCircuitWrapper>

        <VerificationWrapper></VerificationWrapper>

        <BasisGateCircuitWrapper>
          <ImageComponent src={"/placeHolder.png"} />
        </BasisGateCircuitWrapper>
      </RightWrapper>
    </Wrapper>
  )
}
