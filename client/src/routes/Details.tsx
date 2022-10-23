import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Offers } from "../models/offers";

function Details() {
    const { type, id } = useParams()
    const [offers, setOffers] = useState<Offers>();

    useEffect(() => {
        async function fetchOffers() {
            const apiUrl = process.env.REACT_APP_API_URL
            const response = await fetch(`${apiUrl}/offers/${type}/${id}`)
            setOffers(await response.json())
        }

        fetchOffers();
    }, [type, id]);

    return !offers
        ? <p>loading...</p>
        : <div>
            <h1 className='center'>{offers.content.title}</h1>
            <div className='row'>
                <div>
                    <h3 className='center'>Stream</h3>
                    <ul>
                        {Object.keys(offers.stream).map(
                            streamingService => <div>
                                <h4>{streamingService}</h4>
                                {offers.stream[streamingService].map(
                                    country => <li>{country}</li>
                                )}
                            </div>
                        )}
                    </ul>
                </div>
                <div>
                    <h3 className='center'>Rent</h3>
                    {offers.rent.map(
                        offer => <div className='center'>
                            <p>{offer.price.toFixed(2)} kr - {offer.location} - {offer.url}</p>
                        </div>
                    )}
                </div>
                <div>
                    <h3 className='center'>Buy</h3>
                    {offers.buy.map(
                        offer => <div className='center'>
                            <p>{offer.price.toFixed(2)} kr - {offer.location} - {offer.url}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
}

export default Details;
