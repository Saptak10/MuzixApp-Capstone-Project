import React from 'react'

const MusicPlayer = () => {
  return (
    <div>
        <audio controls>
            <source src="horse.ogg" type="audio/ogg" />
            <source src="horse.mp3" type="audio/mpeg" />
            Your browser does not support the audio element.
        </audio>
    </div>
  )
}

export default MusicPlayer