import {
  RouteObject,
  useRoutes
} from 'react-router-dom';
import { useState } from 'react';
import {
  Button,
  Container
} from 'react-bootstrap';
import { Starter, SearchBar, BarLoader } from './Component'

function App(): JSX.Element {

  let routes: RouteObject[] = [
    {
      path: "/",
      element: <Search />
    },
    {
      path: "/result",
      element: <Result />
    },
    {
      path: "/load",
      element: <BarLoader />
    }
  ];

  let element = useRoutes(routes);

  return (
    <div>
      {element}
    </div>
  );
}

function Search() {
  return (
    <Container>
      <Starter />
      <SearchBar />
    </Container>
  );
}
interface props {
  type?: string | null,
  data?: string | null
}

function Result(props: props) {
  const [link, getLink] = useState('https://www.example.com/');

  return (
    <Container>
      <Starter />
      <p>
        Link: <a href={link} target='_blank'>{link}</a>
      </p>
      <h4>{props.type}</h4>
      <p>{props.data}</p>
      <Button
        variant='success'
        className='full'
      >
        Back
      </Button>
    </Container>
  )
}

export default App;
