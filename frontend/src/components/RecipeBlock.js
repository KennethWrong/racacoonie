import React from 'react';


export default function RecipeBlock({title, text}) {
    return(
        <div className="px-6 py-4">
            <div className="font-black text-xl mb-2">{title?title:"NaN"}</div>
            <p className="text-gray-700 text-base font-black">
                {text?text:"NaN"}
            </p>
        </div>
    )
}
